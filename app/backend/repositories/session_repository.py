"""Repository for session data operations."""

from uuid import UUID

import sqlalchemy as sa

from app.backend.database.models import UserSession
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
