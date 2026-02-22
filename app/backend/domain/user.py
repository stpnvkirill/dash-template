from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from flask_login import UserMixin


@dataclass(slots=True)
class PermissionGroupDto:
    name: str
    system_key: str | None


@dataclass(slots=True)
class UserDto(UserMixin):
    id: UUID
    email: str

    first_name: str | None
    last_name: str | None

    sex: str

    session: SessionDto | None = None
    permissions: frozenset[tuple[str, str]] = field(default_factory=frozenset)
    permission_groups: tuple[PermissionGroupDto, ...] = field(default_factory=tuple)

    def get_id(self):
        return self.session.id

    @property
    def created_at(self) -> datetime:
        timestamp_ms = self.id.int >> 80
        return datetime.fromtimestamp(timestamp_ms / 1000.0, tz=UTC)

    def has_permission(self, category: str, key: str) -> bool:
        """Check whether the user has a specific permission."""
        return (category, key) in self.permissions


@dataclass(slots=True)
class SessionDto:
    id: UUID
    is_active: bool
    os: str
    browser: str
    ip: str
    last_active: datetime
