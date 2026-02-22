# Frontend utilities

from __future__ import annotations

from collections.abc import Iterable, Sequence
from functools import wraps
from typing import Protocol

import dash_mantine_components as dmc
from flask_login import current_user

from app.error import PermissionDenied


class PermissionLike(Protocol):
    category: str
    key: str


PermissionInput = PermissionLike | Sequence[str] | str


def _normalize_permission(permission: PermissionInput) -> tuple[str, str]:
    if isinstance(permission, str):
        delimiters = (":", ".")
        for delimiter in delimiters:
            if delimiter in permission:
                category, key = permission.split(delimiter, 1)
                return category.strip(), key.strip()
        raise ValueError(  # noqa: TRY003
            "String permission must use ':' or '.' to separate category and key."
        )

    if isinstance(permission, Sequence):
        if len(permission) != 2:  # noqa: PLR2004
            raise ValueError("Sequence permission must contain category and key.")  # noqa: TRY003
        category, key = permission
        return str(category), str(key)

    if hasattr(permission, "category") and hasattr(permission, "key"):
        return str(permission.category), str(permission.key)

    raise TypeError("Unsupported permission descriptor.")  # noqa: TRY003


def _normalize_permissions(
    permissions: Iterable[PermissionInput],
) -> tuple[tuple[str, str], ...]:
    return tuple(_normalize_permission(permission) for permission in permissions)


def _user_has_permissions(required: tuple[tuple[str, str], ...]) -> bool:
    if not required:
        return True
    if not getattr(current_user, "is_authenticated", False):
        return False
    checker = getattr(current_user, "has_permission", None)
    if not callable(checker):
        return False
    return all(checker(category, key) for category, key in required)


def permission_required(*permissions: PermissionInput):
    """Raise PermissionDenied if current_user lacks any listed permission.

    This decorator checks if the current authenticated user has all specified
    permissions before allowing access to the decorated function. If any
    permission is missing, raises PermissionDenied exception.

    Args:
        *permissions: Permission specifications. Each can be:
            - str: "category:key" or "category.key"
            - tuple: (category, key)
            - PermissionLike object with category and key attributes

    Examples:
        @permission_required("admin:users")
        def delete_user(user_id):
            # Only users with admin:users permission can access
            pass

        @permission_required(("admin", "users"), ("moderator", "content"))
        def moderate_content(content_id):
            # User needs BOTH admin:users AND moderator:content permissions
            pass

        @permission_required("dashboard.view")
        def show_dashboard():
            # Permission using dot notation
            pass

    Raises:
        PermissionDenied: If user lacks any required permission or is not authenticated
    """

    required_permissions = _normalize_permissions(permissions)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not _user_has_permissions(required_permissions):
                raise PermissionDenied()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def hide_if_not_permission(*permissions: PermissionInput):
    """Return an empty Box when the current user lacks any given permission.

    This decorator conditionally renders UI components based on user permissions.
    If the user lacks ANY of the specified permissions, returns an empty dmc.Box().
    Otherwise, renders the original component.

    Useful for hiding UI elements (buttons, menus, sections) that user shouldn't see.

    Args:
        *permissions: Permission specifications. Each can be:
            - str: "category:key" or "category.key"
            - tuple: (category, key)
            - PermissionLike object with category and key attributes

    Returns:
        dmc.Box: Empty box if permissions missing, otherwise original component

    Examples:
        @hide_if_not_permission("admin:users")
        def DeleteUserButton(user_id):
            return dmc.Button("Delete User", color="red")

        @hide_if_not_permission(("admin", "system"), ("moderator", "users"))
        def AdminPanel():
            return dmc.Card([dmc.Text("Admin Controls")])

    Note:
        User must be authenticated. Unauthenticated users will see empty boxes.
    """

    required_permissions = _normalize_permissions(permissions)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not _user_has_permissions(required_permissions):
                return dmc.Box()
            return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["hide_if_not_permission", "permission_required"]
