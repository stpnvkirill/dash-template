"""Service factory for dependency injection.

This module provides a centralized factory for creating service instances
with proper dependency injection, avoiding circular dependencies.
"""

from app.backend.database.models import User, UserSession
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.session_repository import SessionRepository
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.auth.auth_service import AuthService
from app.backend.services.permission.permission_service import PermissionService
from app.backend.services.session.session_service import SessionService
from app.backend.services.user.user_service import UserService


class ServiceFactory:
    """Factory for creating service instances with dependencies.

    This factory creates services with proper dependency injection.
    All services share the same database session manager.
    """

    def __init__(self) -> None:
        """Initialize service factory."""
        self._permission_service: PermissionService | None = None
        self._session_service: SessionService | None = None
        self._auth_service: AuthService | None = None
        self._user_service: UserService | None = None

    @property
    def permission_service(self) -> PermissionService:
        """Get PermissionService instance.

        Returns:
            PermissionService instance.
        """
        if self._permission_service is None:
            self._permission_service = PermissionService()
        return self._permission_service

    @property
    def session_service(self) -> SessionService:
        """Get SessionService instance.

        Returns:
            SessionService instance with injected dependencies.
        """
        if self._session_service is None:
            session_repo = SessionRepository(SqlService(model=UserSession))
            self._session_service = SessionService(
                session_repo=session_repo,
                permission_service=self.permission_service,
            )
        return self._session_service

    @property
    def auth_service(self) -> AuthService:
        """Get AuthService instance.

        Returns:
            AuthService instance with injected dependencies.
        """
        if self._auth_service is None:
            user_repo = UserRepository(SqlService(model=User))
            self._auth_service = AuthService(
                user_repo=user_repo,
                session_service=self.session_service,
            )
        return self._auth_service

    @property
    def user_service(self) -> UserService:
        """Get UserService instance.

        Returns:
            UserService instance with injected dependencies.
        """
        if self._user_service is None:
            user_repo = UserRepository(SqlService(model=User))
            self._user_service = UserService(
                user_repo=user_repo,
                auth_service=self.auth_service,
                session_service=self.session_service,
            )
        return self._user_service


# Global service factory instance
_service_factory: ServiceFactory | None = None


def get_service_factory() -> ServiceFactory:
    """Get global service factory instance.

    Returns:
        ServiceFactory instance.
    """
    global _service_factory
    if _service_factory is None:
        _service_factory = ServiceFactory()
    return _service_factory


def reset_service_factory() -> None:
    """Reset global service factory (useful for testing)."""
    global _service_factory
    _service_factory = None
