from app.backend.database.models import UserSession
from app.backend.domain import SessionDto

from .base_converter import BaseConverter


class SessionConverter(BaseConverter):
    """Converter for sessions"""

    @staticmethod
    def to_dto(session: UserSession) -> SessionDto | None:
        """Convert session to DTO"""
        if not session:
            return None

        return SessionDto(
            id=session.id,
            is_active=session.is_active,
            os=session.os.name if session.os else "unknown",
            browser=session.browser.name if session.browser else "unknown",
            ip=session.ip_address,
            last_active=session.last_activity,
        )
