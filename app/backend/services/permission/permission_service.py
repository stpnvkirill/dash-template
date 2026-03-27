"""Permission service for loading user permissions."""

from uuid import UUID

import sqlalchemy as sa

from app.backend.domain import PermissionGroupDto
from app.backend.queries.permission_queries import PermissionQueries
from app.backend.services.base import BaseService


class PermissionService(BaseService):
    """Service for working with user permissions.

    Provides methods for loading user permissions and permission groups.
    """

    def load_permissions(
        self,
        user_id: UUID,
        session: sa.orm.Session | None = None,
    ) -> frozenset[tuple[str, str]]:
        """Load all user's effective permissions.

        Args:
            user_id: User ID.
            session: Optional SQLAlchemy session (uses new session if not provided).

        Returns:
            Frozen set of (category, key) permission tuples.
        """
        if not user_id:
            return frozenset()

        def execute_query(s: sa.orm.Session) -> frozenset[tuple[str, str]]:
            query = PermissionQueries.get_user_permissions_query(user_id)
            rows = s.execute(query).all()
            return frozenset((row.category, row.key) for row in rows)

        if session is not None:
            return execute_query(session)

        with self.session_scope() as s:
            return execute_query(s)

    def load_permission_groups(
        self,
        user_id: UUID,
        session: sa.orm.Session | None = None,
    ) -> tuple[PermissionGroupDto, ...]:
        """Load user's permission groups.

        Args:
            user_id: User ID.
            session: Optional SQLAlchemy session (uses new session if not provided).

        Returns:
            Tuple of PermissionGroupDto objects.
        """
        if not user_id:
            return ()

        def execute_query(s: sa.orm.Session) -> tuple[PermissionGroupDto, ...]:
            query = PermissionQueries.get_user_permission_groups_query(user_id)
            rows = s.execute(query).all()
            return tuple(
                PermissionGroupDto(name=row.name, system_key=row.system_key)
                for row in rows
            )

        if session is not None:
            return execute_query(session)

        with self.session_scope() as s:
            return execute_query(s)
