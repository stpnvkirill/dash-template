"""Repository for session data operations."""

from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.backend.database.models import OS, Browser, UserSession
from app.backend.infrastructure.database import SqlService

from .base_repository import BaseRepository


class SessionRepository(BaseRepository[UserSession]):
    """Repository for working with user sessions.

    Provides methods for session queries and updates.
    """

    def __init__(self, sql_service: SqlService):
        """Initialize SessionRepository.

        Args:
            sql_service: SqlService instance for database operations.
        """
        super().__init__(sql_service)

    def get_active_sessions(
        self, user_id: UUID, exclude_id: UUID | None = None
    ) -> list[UserSession]:
        """Get user's active sessions.

        Args:
            user_id: User ID.
            exclude_id: Session ID to exclude (optional).

        Returns:
            List of active UserSession instances.
        """
        conditions = [UserSession.user_id == user_id, UserSession.is_active]
        if exclude_id:
            conditions.append(UserSession.id != exclude_id)

        return self.sql_service.select(*conditions)

    def deactivate_session(self, session_id: UUID) -> UserSession | None:
        """Deactivate session.

        Args:
            session_id: Session ID to deactivate.

        Returns:
            Updated UserSession instance or None if not found.
        """
        return self.update(session_id, is_active=False)

    def update_activity(self, session_id: UUID) -> UserSession | None:
        """Update session activity time.

        Args:
            session_id: Session ID to update.

        Returns:
            Updated UserSession instance or None if not found.
        """
        return self.sql_service.update(
            id=session_id,
            last_activity=sa.func.now(),
            request_count=UserSession.request_count + 1,
        )

    def ensure_os_exists(self, session: sa.orm.Session, os_name: str | None) -> UUID:
        """Ensure OS exists in database, create if needed.

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

    def ensure_browser_exists(
        self, session: sa.orm.Session, browser_name: str | None
    ) -> UUID:
        """Ensure browser exists in database, create if needed.

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

    def create_session_record(
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
