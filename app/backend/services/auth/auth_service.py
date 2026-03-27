"""Authentication service for user login and registration."""

from werkzeug.security import check_password_hash

from app.backend.database.models import User
from app.backend.domain import UserDto
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.base import BaseService


class AuthService(BaseService):
    """Service for user authentication.

    Handles user login, password verification, and email availability checks.
    """

    def __init__(self, user_repo: UserRepository | None = None):
        """Initialize AuthService.

        Args:
            user_repo: UserRepository instance (optional, created if not provided).
        """
        super().__init__()
        self.user_repo: UserRepository = user_repo or UserRepository(
            SqlService(model=User)
        )

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
            UserDto with session info if authentication successful, None otherwise.
        """
        user = self.user_repo.get_by_email(email)

        if user and check_password_hash(user.password, password):
            # Import here to avoid circular dependency
            from app.backend.services.session.session_service import (  # noqa: PLC0415
                SessionService,
            )

            session_service = SessionService()
            return session_service.create_session(
                user=user,
                ip=ip,
                os=os,
                browser=browser,
            )

        return None

    def check_email_available(self, email: str) -> bool:
        """Check email availability for registration.

        Args:
            email: Email address to check.

        Returns:
            True if email is available, False if already registered.
        """
        return self.user_repo.is_email_available(email)
