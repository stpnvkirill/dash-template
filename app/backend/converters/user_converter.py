from typing import TYPE_CHECKING

from app.backend.database.models import User
from app.backend.domain import SessionDto, UserDto

if TYPE_CHECKING:
    pass

from .base_converter import BaseConverter


class UserConverter(BaseConverter):
    """Converter for users"""

    @staticmethod
    def to_dto(
        user: User | UserDto,
        session: SessionDto | None = None,
        permissions: frozenset[tuple[str, str]] | None = None,
        permission_groups: tuple | None = None,
    ) -> UserDto | None:
        """Convert user to DTO"""
        if not user:
            return None

        # Determine permissions
        resolved_permissions = (
            permissions
            if permissions is not None
            else user.permissions
            if isinstance(user, UserDto)
            else frozenset()
        )

        # Determine permission groups
        resolved_groups = (
            permission_groups
            if permission_groups is not None
            else user.permission_groups
            if isinstance(user, UserDto)
            else ()
        )

        # Determine sex
        sex_value = (
            user.sex
            if isinstance(user.sex, str)
            else user.sex.value
            if hasattr(user.sex, "value")
            else user.sex
        )

        return UserDto(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            sex=sex_value,
            session=session,  # Use passed session
            permissions=resolved_permissions,
            permission_groups=resolved_groups,
        )
