"""Backend module with service registry.

This module provides a central registry for all backend services.
Services are instantiated lazily to avoid circular dependencies.
"""

from .services.user.user_service import UserService


class Backend:
    """Central registry for backend services.

    Provides access to all application services through a single interface.
    Services are instantiated on first access to avoid circular dependencies.
    """

    def __init__(self) -> None:
        """Initialize Backend service registry."""
        self._user: UserService | None = None

    @property
    def user(self) -> UserService:
        """Get UserService instance.

        Returns:
            UserService instance (created on first access).
        """
        if self._user is None:
            self._user = UserService()
        return self._user


# Global service registry instance
# Note: This is a legacy pattern. New code should use dependency injection.
back = Backend()
