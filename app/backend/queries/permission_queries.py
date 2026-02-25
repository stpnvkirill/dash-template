from uuid import UUID

import sqlalchemy as sa

from app.backend.database.models import (
    Permission,
    PermissionGroup,
    permission_group_permissions,
    user_permission_groups,
    user_permissions,
)


class PermissionQueries:
    """Query builders for working with permissions"""

    @staticmethod
    def get_user_direct_permissions_query(user_id: UUID) -> sa.Select:
        """Query to get user's direct permissions"""
        return (
            sa.select(Permission.category, Permission.key)
            .select_from(
                user_permissions.join(
                    Permission,
                    user_permissions.c.permission_id == Permission.id,
                )
            )
            .where(user_permissions.c.user_id == user_id)
        )

    @staticmethod
    def get_user_group_permissions_query(user_id: UUID) -> sa.Select:
        """Query to get permissions through groups"""
        return (
            sa.select(Permission.category, Permission.key)
            .select_from(
                user_permission_groups.join(
                    permission_group_permissions,
                    user_permission_groups.c.group_id
                    == permission_group_permissions.c.group_id,
                ).join(
                    Permission,
                    permission_group_permissions.c.permission_id == Permission.id,
                )
            )
            .where(user_permission_groups.c.user_id == user_id)
        )

    @staticmethod
    def get_user_permissions_query(user_id: UUID) -> sa.Select:
        """Combined query to get all user permissions"""
        direct_query = PermissionQueries.get_user_direct_permissions_query(user_id)
        group_query = PermissionQueries.get_user_group_permissions_query(user_id)

        combined = sa.union_all(direct_query, group_query).alias(
            "user_permissions_union"
        )

        return sa.select(
            combined.c.category,
            combined.c.key,
        ).distinct()

    @staticmethod
    def get_user_permission_groups_query(user_id: UUID) -> sa.Select:
        """Query to get user's permission groups"""
        return (
            sa.select(PermissionGroup.name, PermissionGroup.system_key)
            .select_from(
                user_permission_groups.join(
                    PermissionGroup,
                    user_permission_groups.c.group_id == PermissionGroup.id,
                )
            )
            .where(user_permission_groups.c.user_id == user_id)
            .order_by(PermissionGroup.name)
        )
