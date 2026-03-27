"""User service for managing user accounts and profiles."""

import logging
from typing import Literal
from uuid import UUID

from app.backend.converters.user_converter import UserConverter
from app.backend.database.models import User
from app.backend.domain import UserDto
from app.backend.domain.validators import PasswordValidator
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.auth.auth_service import AuthService
from app.backend.services.base import BaseService
from app.backend.services.session.session_service import SessionService

logger = logging.getLogger(__name__)


class UserService(BaseService):
    """Service for managing users.

    Provides methods for user CRUD operations, authentication, and session management.
    """

    def __init__(
        self,
        user_repo: UserRepository | None = None,
        auth_service: AuthService | None = None,
        session_service: SessionService | None = None,
    ):
        """Initialize UserService.

        Args:
            user_repo: UserRepository instance (optional, created if not provided).
            auth_service: AuthService instance for authentication.
            session_service: SessionService instance for session management.
        """
        super().__init__()
        self.user_repo: UserRepository = user_repo or UserRepository(
            SqlService(model=User)
        )
        self._auth_service = auth_service
        self._session_service = session_service

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        sex: Literal["MALE", "FEMALE", "NOT_SPECIFIED"] = "NOT_SPECIFIED",
    ) -> UserDto | None:
        """Create new user account.

        Args:
            email: User email address.
            password: Plain text password.
            first_name: User first name.
            last_name: User last name.
            sex: User sex (default: NOT_SPECIFIED).

        Returns:
            UserDto if created successfully, None otherwise.
        """
        # Validate password strength
        password_result = PasswordValidator.validate(password)
        if not password_result.is_valid:
            logger.warning(
                f"Password validation failed for user {email}: "
                f"{password_result.error_message}"
            )
            return None

        try:
            logger.info(f"Creating user: {email}")
            user = self.user_repo.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                sex=sex,
            )
            logger.info(f"User created successfully: {user.id}")
            return UserConverter.to_dto(user)
        except ValueError as e:
            logger.warning(f"Failed to create user {email}: {e}")
            return None

    def get_user(self, user_id: UUID) -> UserDto | None:
        """Get user by ID.

        Args:
            user_id: User ID.

        Returns:
            UserDto if found, None otherwise.
        """
        user = self.user_repo.get_by_id(user_id)
        return UserConverter.to_dto(user)

    def update_user(
        self,
        user_id: UUID,
        first_name: str,
        last_name: str,
        sex: str,
        password: str | None = None,
    ) -> UserDto | None:
        """Update user profile.

        Args:
            user_id: User ID.
            first_name: New first name.
            last_name: New last name.
            sex: New sex value.
            password: New password (optional).

        Returns:
            Updated UserDto if successful, None otherwise.
        """
        user = self.user_repo.update_user(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            password=password,
        )
        return UserConverter.to_dto(user)

    def check_email_available(self, email: str) -> bool:
        """Check email availability for registration.

        Args:
            email: Email address to check.

        Returns:
            True if email is available, False if already registered.
        """
        return self.user_repo.is_email_available(email)

    def authenticate(
        self,
        email: str,
        password: str,
        ip: str | None = None,
        os: str | None = None,
        browser: str | None = None,
    ) -> UserDto | None:
        """Authenticate user and create session.

        Args:
            email: User email address.
            password: Plain text password.
            ip: Client IP address.
            os: Client operating system.
            browser: Client browser.

        Returns:
            UserDto with session info if successful, None otherwise.
        """
        return self._auth_service.authenticate(
            email=email,
            password=password,
            ip=ip,
            os=os,
            browser=browser,
        )

    def get_user_by_session(self, session_id: UUID) -> UserDto | None:
        """Get user by session ID.

        Args:
            session_id: Session ID.

        Returns:
            UserDto if found, None otherwise.
        """
        return self._session_service.get_user_by_session(session_id)

    def create_session(
        self,
        user: UserDto | User,
        ip: str | None,
        os: str | None = None,
        browser: str | None = None,
    ) -> UserDto:
        """Create session for user.

        Args:
            user: User object or UserDto.
            ip: Client IP address.
            os: Client operating system.
            browser: Client browser.

        Returns:
            UserDto with session info.
        """
        return self._session_service.create_session(
            user=user,
            ip=ip,
            os=os,
            browser=browser,
        )

    def deactivate_session(self, session_id: UUID) -> bool:
        """Deactivate session.

        Args:
            session_id: Session ID to deactivate.

        Returns:
            True if session was deactivated, False if not found.
        """
        return self._session_service.deactivate_session(session_id)

    def get_active_sessions(
        self, user_id: UUID, exclude_id: UUID | None = None
    ) -> list:
        """Get user's active sessions.

        Args:
            user_id: User ID.
            exclude_id: Session ID to exclude (optional).

        Returns:
            List of SessionDto objects.
        """
        return self._session_service.get_active_sessions(user_id, exclude_id)
