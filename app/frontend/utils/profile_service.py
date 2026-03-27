"""User profile management service for frontend.

Extracts profile update business logic from Dash callbacks,
providing better testability and separation of concerns.
"""

from dataclasses import dataclass
from uuid import UUID

from app.backend import back
from app.backend.domain import UserDto


@dataclass(frozen=True)
class ProfileUpdateData:
    """Profile update data.

    Attributes:
        user_id: User ID.
        first_name: First name.
        last_name: Last name.
        sex: Sex (optional).
        password: New password (optional, empty string = no change).
    """

    user_id: UUID
    first_name: str
    last_name: str
    sex: str | None = None
    password: str | None = None


class FrontendProfileService:
    """Profile management service for frontend.

    Encapsulates user data update logic.
    """

    @staticmethod
    def update_profile(data: ProfileUpdateData) -> UserDto:
        """Update user profile data.

        Args:
            data: Update data.

        Returns:
            Updated user object.
        """
        return back.user.update_user(
            user_id=data.user_id,
            first_name=data.first_name,
            last_name=data.last_name,
            password=data.password if data.password else None,
            sex=data.sex,
        )

    @staticmethod
    def get_active_sessions(user_id: UUID, exclude_id: UUID | None = None) -> list:
        """Get active user sessions.

        Args:
            user_id: User ID.
            exclude_id: Exclude session with this ID (optional).

        Returns:
            List of active sessions.
        """
        return back.user.get_active_sessions(user_id, exclude_id=exclude_id)

    @staticmethod
    def deactivate_session(session_id: UUID) -> None:
        """Deactivate session.

        Args:
            session_id: Session ID to deactivate.
        """
        back.user.deactivate_session(session_id=session_id)

    @staticmethod
    def deactivate_all_other_sessions(user_id: UUID, current_session_id: UUID) -> None:
        """Deactivate all sessions except current.

        Args:
            user_id: User ID.
            current_session_id: Current session ID (do not deactivate).
        """
        sessions = back.user.get_active_sessions(user_id, exclude_id=current_session_id)
        for session in sessions:
            back.user.deactivate_session(session_id=session.id)
