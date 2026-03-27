"""Lazy loader for user permissions and groups."""

from flask import g
from flask_login import current_user

from app.backend.domain import UserDto
from app.backend.services.factory import get_service_factory


class LazyUserLoader:
    """Lazy loader for user permissions and groups.

    Provides methods for loading user permissions and permission groups
    on-demand with caching in flask.g.
    """

    @staticmethod
    def with_permissions() -> UserDto:
        """Get current_user with lazily loaded permissions and groups.

        Permissions are loaded from database only on first call during request.
        Subsequent calls use cached values from flask.g.

        Returns:
            UserDto with loaded permissions and permission_groups.
        """
        if "permissions" not in g:
            factory = get_service_factory()
            g.permissions = factory.permission_service.load_permissions(current_user.id)
            g.permission_groups = factory.permission_service.load_permission_groups(
                current_user.id
            )

        current_user.permissions = g.permissions
        current_user.permission_groups = g.permission_groups
        return current_user
