from uuid import UUID

from app.backend.database.models import UserSession
from app.backend.services.base import SqlService

from .base_repository import BaseRepository


class SessionRepository(BaseRepository[UserSession]):
    """Repository for working with sessions"""

    def __init__(self, sql_service: SqlService):
        super().__init__(sql_service)

    def get_active_sessions(
        self, user_id: UUID, exclude_id: UUID | None = None
    ) -> list[UserSession]:
        """Get user's active sessions"""
        conditions = [UserSession.user_id == user_id, UserSession.is_active]
        if exclude_id:
            conditions.append(UserSession.id != exclude_id)

        return self.sql_service.select(*conditions)

    def deactivate_session(self, session_id: UUID) -> UserSession | None:
        """Deactivate session"""
        return self.update(session_id, is_active=False)

    def update_activity(self, session_id: UUID) -> UserSession | None:
        """Update session activity time"""
        return self.sql_service.update(
            id=session_id,
            last_activity=self.sql_service.model.last_activity,  # Will be set to NOW()
            request_count=self.sql_service.model.request_count + 1,
        )
