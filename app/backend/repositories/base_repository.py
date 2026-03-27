"""Base repository for data operations.

Repositories are responsible for data access and should use SqlService
for low-level database operations.
"""

from typing import TypeVar
from uuid import UUID

from app.backend.infrastructure.database import SqlService

T = TypeVar("T")


class BaseRepository[T]:
    """Base repository for data operations.

    Type parameter T represents the model type this repository works with.
    """

    def __init__(self, sql_service: SqlService):
        """Initialize repository with SqlService.

        Args:
            sql_service: SqlService instance for database operations.
        """
        self.sql_service: SqlService = sql_service

    def get_by_id(self, id: UUID) -> T | None:
        """Get object by ID.

        Args:
            id: Object ID.

        Returns:
            Object instance or None if not found.
        """
        return self.sql_service.get(id=id)

    def create(self, **kwargs: object) -> T:
        """Create new object.

        Args:
            **kwargs: Object field values.

        Returns:
            Created object instance.
        """
        return self.sql_service.insert(**kwargs)

    def update(self, id: UUID, **kwargs: object) -> T:
        """Update object.

        Args:
            id: Object ID.
            **kwargs: Fields to update.

        Returns:
            Updated object instance.
        """
        return self.sql_service.update(id=id, **kwargs)

    def delete(self, id: UUID) -> bool:
        """Delete object.

        Args:
            id: Object ID.

        Returns:
            True if object was deleted, False if not found.
        """
        return self.sql_service.delete(id=id)
