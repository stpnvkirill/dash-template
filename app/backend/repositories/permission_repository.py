from app.backend.database.models import Permission, PermissionGroup
from app.backend.services.base import SqlService

from .base_repository import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    """Repository for working with permissions"""

    def __init__(self, sql_service: SqlService):
        super().__init__(sql_service)


class PermissionGroupRepository(BaseRepository[PermissionGroup]):
    """Repository for working with permission groups"""

    def __init__(self, sql_service: SqlService):
        super().__init__(sql_service)
