"""Session service for managing user sessions."""

from uuid import UUID

import sqlalchemy as sa

from app.backend.converters.session_converter import SessionConverter
from app.backend.converters.user_converter import UserConverter
from app.backend.database.models import User, UserSession
from app.backend.domain import PermissionGroupDto, SessionDto, UserDto
from app.backend.infrastructure.database import SqlService
from app.backend.queries.permission_queries import PermissionQueries
from app.backend.repositories.session_repository import SessionRepository
from app.backend.services.base import BaseService
from app.backend.services.permission.permission_service import PermissionService


class SessionService(BaseService):
    """Service for managing user sessions.

    Handles session creation, validation, and lifecycle management.
    """

    def __init__(
        self,
        session_repo: SessionRepository | None = None,
        permission_service: PermissionService | None = None,
    ):
        """Initialize SessionService.

        Args:
            session_repo: SessionRepository (optional, created if not provided).
            permission_service: PermissionService for loading user permissions.
        """
        super().__init__()
        if session_repo:
            self.session_repo: SessionRepository = session_repo
        else:
            self.session_repo = SessionRepository(SqlService(model=UserSession))
        self._permission_service = permission_service or PermissionService()

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
            # Use repository methods for OS/browser lookup
            os_id = self.session_repo.ensure_os_exists(session, os)
            browser_id = self.session_repo.ensure_browser_exists(session, browser)
            session_id = self.session_repo.create_session_record(
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
        query = PermissionQueries.get_user_permissions_query(user_id)
        rows = session.execute(query).all()
        return frozenset((row.category, row.key) for row in rows)

    def _load_permission_groups(
        self, user_id: UUID, session: sa.orm.Session
    ) -> tuple[PermissionGroupDto, ...]:
        """Load user permission groups.

        Args:
            user_id: User ID.
            session: SQLAlchemy session.

        Returns:
            Tuple of PermissionGroupDto objects.
        """
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

    def deactivate_all_other_sessions(
        self, user_id: UUID, exclude_session_id: UUID
    ) -> int:
        """Deactivate all user sessions except specified one.

        Args:
            user_id: User ID.
            exclude_session_id: Session ID to keep active.

        Returns:
            Number of deactivated sessions.
        """
        return self.session_repo.deactivate_all_except(user_id, exclude_session_id)

    def get_active_sessions(
        self,
        user_id: UUID,
        exclude_id: UUID | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[SessionDto]:
        """Get user's active sessions.

        Args:
            user_id: User ID.
            exclude_id: Session ID to exclude (optional).
            limit: Maximum number of sessions to return (default: 50).
            offset: Number of sessions to skip (default: 0).

        Returns:
            List of SessionDto objects.
        """
        sessions = self.session_repo.get_active_sessions(
            user_id, exclude_id, limit, offset
        )
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
