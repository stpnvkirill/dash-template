from typing import TypeVar
from uuid import UUID

from app.backend.services.base import SqlService

T = TypeVar("T")


class BaseRepository[T]:
    """Base repository for data operations"""

    def __init__(self, sql_service: SqlService):
        self.sql_service = sql_service

    def get_by_id(self, id: UUID) -> T | None:
        """Get object by ID"""
        return self.sql_service.get(id=id)

    def get_all(self) -> list[T]:
        """Get all objects"""
        return self.sql_service.select()

    def create(self, **kwargs) -> T:
        """Create new object"""
        return self.sql_service.insert(**kwargs)

    def update(self, id: UUID, **kwargs) -> T:
        """Update object"""
        return self.sql_service.update(id=id, **kwargs)

    def delete(self, id: UUID) -> bool:
        """Delete object"""
        return self.sql_service.delete(id=id)
