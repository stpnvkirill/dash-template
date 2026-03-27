"""Converter for UserSession model to SessionDto."""

from app.backend.database.models import UserSession
from app.backend.domain import SessionDto

from .base_converter import BaseConverter


class SessionConverter(BaseConverter[UserSession, SessionDto]):
    """Converter for UserSession model to SessionDto."""

    @staticmethod
    def to_dto(session: UserSession) -> SessionDto | None:
        """Convert session to DTO.

        Args:
            session: UserSession model instance.

        Returns:
            SessionDto if session is valid, None otherwise.
        """
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

    @staticmethod
    def from_dto(_dto: SessionDto) -> UserSession | None:
        """Convert SessionDto to model (not implemented).

        Args:
            _dto: SessionDto instance.

        Returns:
            None (conversion from DTO to model not supported).
        """
        return None
