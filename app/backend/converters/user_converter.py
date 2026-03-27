"""Converter for User model to UserDto."""

from app.backend.database.models import User
from app.backend.domain import SessionDto, UserDto

from .base_converter import BaseConverter


class UserConverter(BaseConverter[User, UserDto]):
    """Converter for User model to UserDto."""

    @staticmethod
    def to_dto(
        user: User | UserDto,
        session: SessionDto | None = None,
        permissions: frozenset[tuple[str, str]] | None = None,
        permission_groups: tuple | None = None,
    ) -> UserDto | None:
        """Convert user to DTO.

        Args:
            user: User model or UserDto to convert.
            session: Optional session DTO.
            permissions: Optional permissions set.
            permission_groups: Optional permission groups tuple.

        Returns:
            UserDto if user is valid, None otherwise.
        """
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

        # Determine sex value (handle both string and enum)
        sex_value = getattr(user.sex, "value", str(user.sex))

        return UserDto(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            sex=sex_value,
            session=session,
            permissions=resolved_permissions,
            permission_groups=resolved_groups,
        )

    @staticmethod
    def from_dto(_dto: UserDto) -> User | None:
        """Convert UserDto to model (not implemented).

        Args:
            _dto: UserDto instance.

        Returns:
            None (conversion from DTO to model not supported).
        """
        # This converter is primarily for model -> DTO conversion
        # DTO -> model conversion would require additional logic
        return None
