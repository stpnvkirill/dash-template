"""Session service for managing user sessions."""

from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.backend.converters.session_converter import SessionConverter
from app.backend.converters.user_converter import UserConverter
from app.backend.database.models import OS, Browser, User, UserSession
from app.backend.domain import SessionDto, UserDto
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.session_repository import SessionRepository
from app.backend.services.base import BaseService


class SessionService(BaseService):
    """Service for managing user sessions.

    Handles session creation, validation, and lifecycle management.
    """

    def __init__(self, session_repo: SessionRepository | None = None):
        """Initialize SessionService.

        Args:
            session_repo: SessionRepository (optional, created if not provided).
        """
        super().__init__()
        self.session_repo: SessionRepository = session_repo or SessionRepository(
            SqlService(model=UserSession)
        )

    def create_session(
        self,
        user: UserDto | User,
        ip: str | None,
        os: str | None = None,
        browser: str | None = None,
    ) -> UserDto:
        """Create new session for user.

        Args:
            user: User object or UserDto.
            ip: Client IP address.
            os: Client operating system.
            browser: Client browser.

        Returns:
            UserDto with updated session information.
        """
        with self.session_scope() as session:
            os_id = self._ensure_os_exists(session, os)
            browser_id = self._ensure_browser_exists(session, browser)
            session_id = self._create_session_record(
                session, user.id, ip, os_id, browser_id
            )

            # Get created session
            user_session = session.scalar(
                sa.select(UserSession).where(UserSession.id == session_id)
            )

            # Load permissions
            permissions = self._load_permissions(user.id, session)
            permission_groups = self._load_permission_groups(user.id, session)

            # Convert session to DTO
            session_dto = (
                SessionConverter.to_dto(user_session) if user_session else None
            )

            if user_session:
                session.expunge(user_session)

            return UserConverter.to_dto(
                user=user,
                session=session_dto,
                permissions=permissions,
                permission_groups=permission_groups,
            )

    def _ensure_os_exists(self, session: sa.orm.Session, os_name: str | None) -> UUID:
        """Ensure OS exists, create if needed.

        Args:
            session: SQLAlchemy session.
            os_name: Operating system name.

        Returns:
            OS record UUID.
        """
        os_name = sa.func.lower(os_name or "unknown")

        os_cte = (
            pg_insert(OS)
            .values(name=os_name)
            .on_conflict_do_update(index_elements=["name"], set_={"name": os_name})
            .returning(OS.id)
            .cte("os_cte")
        )

        return session.scalar(sa.select(os_cte.c.id))

    def _ensure_browser_exists(
        self, session: sa.orm.Session, browser_name: str | None
    ) -> UUID:
        """Ensure browser exists, create if needed.

        Args:
            session: SQLAlchemy session.
            browser_name: Browser name.

        Returns:
            Browser record UUID.
        """
        browser_name = sa.func.lower(browser_name or "unknown")

        browser_cte = (
            pg_insert(Browser)
            .values(name=browser_name)
            .on_conflict_do_update(index_elements=["name"], set_={"name": browser_name})
            .returning(Browser.id)
            .cte("browser_cte")
        )

        return session.scalar(sa.select(browser_cte.c.id))

    def _create_session_record(
        self,
        session: sa.orm.Session,
        user_id: UUID,
        ip: str | None,
        os_id: UUID,
        browser_id: UUID,
    ) -> UUID:
        """Create session record in database.

        Args:
            session: SQLAlchemy session.
            user_id: User ID.
            ip: Client IP address.
            os_id: OS record ID.
            browser_id: Browser record ID.

        Returns:
            Created session UUID.
        """
        return session.scalar(
            pg_insert(UserSession)
            .values(
                user_id=user_id,
                ip_address=ip,
                os_id=os_id,
                browser_id=browser_id,
            )
            .returning(UserSession.id)
        )

    def _load_permissions(
        self, user_id: UUID, session: sa.orm.Session
    ) -> frozenset[tuple[str, str]]:
        """Load user permissions.

        Args:
            user_id: User ID.
            session: SQLAlchemy session.

        Returns:
            Frozen set of (category, key) permission tuples.
        """
        # Import here to avoid circular dependency
        from app.backend.queries.permission_queries import (  # noqa: PLC0415
            PermissionQueries,
        )

        query = PermissionQueries.get_user_permissions_query(user_id)
        rows = session.execute(query).all()
        return frozenset((row.category, row.key) for row in rows)

    def _load_permission_groups(self, user_id: UUID, session: sa.orm.Session) -> tuple:
        """Load user permission groups.

        Args:
            user_id: User ID.
            session: SQLAlchemy session.

        Returns:
            Tuple of PermissionGroupDto objects.
        """
        # Import here to avoid circular dependency
        from app.backend.domain import PermissionGroupDto  # noqa: PLC0415
        from app.backend.queries.permission_queries import (  # noqa: PLC0415
            PermissionQueries,
        )

        query = PermissionQueries.get_user_permission_groups_query(user_id)
        rows = session.execute(query).all()
        return tuple(
            PermissionGroupDto(name=row.name, system_key=row.system_key) for row in rows
        )

    def deactivate_session(self, session_id: UUID) -> bool:
        """Deactivate session.

        Args:
            session_id: Session ID to deactivate.

        Returns:
            True if session was deactivated, False if not found.
        """
        result = self.session_repo.deactivate_session(session_id)
        return result is not None

    def get_active_sessions(
        self, user_id: UUID, exclude_id: UUID | None = None
    ) -> list[SessionDto]:
        """Get user's active sessions.

        Args:
            user_id: User ID.
            exclude_id: Session ID to exclude (optional).

        Returns:
            List of SessionDto objects.
        """
        sessions = self.session_repo.get_active_sessions(user_id, exclude_id)
        return [SessionConverter.to_dto(session) for session in sessions]

    def get_user_by_session(self, session_id: UUID) -> UserDto | None:
        """Get user by session ID with activity update.

        Args:
            session_id: Session ID.

        Returns:
            UserDto with session info, or None if session not found.
        """
        permissions: frozenset[tuple[str, str]] = frozenset()
        permission_groups: tuple = ()

        with self.session_scope() as session:
            # Update session activity and get user
            update_subq = (
                sa.update(UserSession)
                .where(
                    UserSession.id == session_id,
                    UserSession.is_active,
                )
                .values(
                    last_activity=sa.func.now(),
                    request_count=UserSession.request_count + 1,
                )
                .returning(UserSession.user_id)
                .cte("updated_session_ids")
            )

            stmt = sa.select(User).join(update_subq, User.id == update_subq.c.user_id)
            user = session.scalar(stmt)

            # Get updated session
            user_session = session.scalar(
                sa.select(UserSession).where(UserSession.id == session_id)
            )

            if user:
                permissions = self._load_permissions(user.id, session)
                permission_groups = self._load_permission_groups(user.id, session)

            # Convert session to DTO
            session_dto = (
                SessionConverter.to_dto(user_session) if user_session else None
            )

            return UserConverter.to_dto(
                user=user,
                session=session_dto,
                permissions=permissions,
                permission_groups=permission_groups,
            )
