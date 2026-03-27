"""Authentication service for user login and registration."""

import logging

from werkzeug.security import check_password_hash

from app.backend.database.models import User
from app.backend.domain import UserDto
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.base import BaseService
from app.backend.services.rate_limiter import get_auth_rate_limiter
from app.backend.services.session.session_service import SessionService

logger = logging.getLogger(__name__)


class AuthService(BaseService):
    """Service for user authentication.

    Handles user login, password verification, and email availability checks.
    Includes rate limiting to protect against brute-force attacks.
    """

    def __init__(
        self,
        user_repo: UserRepository | None = None,
        session_service: SessionService | None = None,
    ):
        """Initialize AuthService.

        Args:
            user_repo: UserRepository instance (optional, created if not provided).
            session_service: SessionService instance for session creation.
        """
        super().__init__()
        self.user_repo: UserRepository = user_repo or UserRepository(
            SqlService(model=User)
        )
        self._session_service = session_service
        self._rate_limiter = get_auth_rate_limiter()

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

        Raises:
            RateLimitExceeded: If too many failed attempts.
        """
        # Check rate limit using email and IP
        identifiers = [email.lower()]
        if ip:
            identifiers.append(f"ip:{ip}")

        # Check if any identifier is blocked
        for identifier in identifiers:
            if self._rate_limiter.is_blocked(identifier):
                retry_after = self._rate_limiter.get_retry_after(identifier)
                logger.warning(
                    f"Authentication rate limited for {identifier}. "
                    f"Retry after {retry_after}s"
                )
                return None

        # Record attempt for all identifiers
        for identifier in identifiers:
            self._rate_limiter.record_attempt(identifier)

        user = self.user_repo.get_by_email(email)

        if user and check_password_hash(user.password, password):
            # Successful login - reset rate limit
            for identifier in identifiers:
                self._rate_limiter.reset(identifier)

            return self._session_service.create_session(
                user=user,
                ip=ip,
                os=os,
                browser=browser,
            )

        logger.warning(
            f"Failed authentication attempt for {email}. "
            f"Remaining attempts: {self._rate_limiter.get_remaining_attempts(email)}"
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
