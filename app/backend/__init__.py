"""Backend module with service registry.

This module provides a central registry for all backend services
using the ServiceFactory pattern for dependency injection.
"""

from .services.factory import ServiceFactory, get_service_factory

# Global service factory instance
# Note: Use get_service_factory() for access to services
_service_factory: ServiceFactory | None = None


def get_factory() -> ServiceFactory:
    """Get global service factory instance.

    Returns:
        ServiceFactory instance for creating services.
    """
    global _service_factory  # noqa: PLW0603
    if _service_factory is None:
        _service_factory = get_service_factory()
    return _service_factory


# Legacy compatibility - keep 'back' for existing code
class _BackendCompat:
    """Backward compatibility wrapper for legacy code."""

    @property
    def user(self):
        """Get UserService (legacy compatibility)."""
        return get_factory().user_service


back = _BackendCompat()
