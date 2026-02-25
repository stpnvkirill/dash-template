from uuid import UUID

import sqlalchemy as sa

from app.backend.converters.session_converter import SessionConverter
from app.backend.converters.user_converter import UserConverter
from app.backend.database.models import OS, Browser, User, UserSession
from app.backend.domain import SessionDto, UserDto
from app.backend.repositories.session_repository import SessionRepository
from app.backend.services.base import BaseService, SqlService, pg_insert
from app.backend.services.permission.permission_service import PermissionService


class SessionService(BaseService):
    """Service for managing user sessions"""

    def __init__(self):
        super().__init__()
        self.session_repo = SessionRepository(SqlService(model=UserSession))
        self.permission_service = PermissionService()

    def create_session(
        self,
        user: UserDto | User,
        ip: str | None,
        os: str | None = None,
        browser: str | None = None,
    ) -> UserDto:
        """Create new session for user"""
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
            permissions = self.permission_service.load_permissions(user.id, session)
            permission_groups = self.permission_service.load_permission_groups(
                user.id, session
            )

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
        """Ensure OS exists, create if needed"""
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
        """Ensure browser exists, create if needed"""
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
        """Create session record"""
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

    def deactivate_session(self, session_id: UUID) -> bool:
        """Deactivate session"""
        result = self.session_repo.deactivate_session(session_id)
        return result is not None

    def get_active_sessions(
        self, user_id: UUID, exclude_id: UUID | None = None
    ) -> list[SessionDto]:
        """Get user's active sessions"""
        sessions = self.session_repo.get_active_sessions(user_id, exclude_id)
        return [SessionConverter.to_dto(session) for session in sessions]

    def get_user_by_session(self, session_id: UUID) -> UserDto | None:
        """Get user by session ID with activity update"""
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
                permissions = self.permission_service.load_permissions(user.id, session)
                permission_groups = self.permission_service.load_permission_groups(
                    user.id, session
                )

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
