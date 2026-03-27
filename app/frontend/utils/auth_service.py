"""Authentication service for frontend.

Extracts authentication business logic from Dash callbacks,
providing better testability and separation of concerns.
"""

from dataclasses import dataclass

from flask import g

from app.backend import back
from app.backend.domain import UserDto

type AuthResult = tuple[UserDto | None, str | None]


@dataclass(frozen=True)
class LoginCredentials:
    """Login credentials.

    Attributes:
        email: User email.
        password: Password in plain text.
        remember: Remember me flag.
        ip_address: Client IP address.
        os: Client operating system.
        browser: Client browser.
    """

    email: str
    password: str
    remember: bool
    ip_address: str
    os: str
    browser: str


@dataclass(frozen=True)
class LoginResult:
    """Login attempt result.

    Attributes:
        success: Success flag.
        user: User object (if success).
        error_message: Error message (if failure).
    """

    success: bool
    user: UserDto | None = None
    error_message: str | None = None


class FrontendAuthService:
    """Authentication service for frontend.

    Encapsulates credential verification and session creation logic.
    """

    @staticmethod
    def authenticate(credentials: LoginCredentials) -> LoginResult:
        """Authenticate user by credentials.

        Args:
            credentials: Login credentials.

        Returns:
            LoginResult with success or error information.
        """
        user = back.user.authenticate(
            email=credentials.email,
            password=credentials.password,
            ip=credentials.ip_address,
            os=credentials.os,
            browser=credentials.browser,
        )

        if not user:
            return LoginResult(
                success=False,
                error_message="Invalid email or password",
            )

        return LoginResult(success=True, user=user)

    @staticmethod
    def get_client_info() -> dict[str, str]:
        """Get client info from Flask context.

        Returns:
            Dict with keys: ip_address, os, browser.
        """
        os_family = "unknown"
        browser_family = "unknown"

        if hasattr(g, "user_agent"):
            if hasattr(g.user_agent, "os"):
                os_family = getattr(g.user_agent.os, "family", "unknown")
            if hasattr(g.user_agent, "browser"):
                browser_family = getattr(g.user_agent.browser, "family", "unknown")

        return {
            "ip_address": getattr(g, "ip_address", "unknown"),
            "os": os_family,
            "browser": browser_family,
        }
