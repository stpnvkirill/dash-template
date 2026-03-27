from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol, runtime_checkable
from uuid import UUID


@runtime_checkable
class UserSessionProtocol(Protocol):
    """Protocol for user session objects compatible with Flask-Login."""

    id: UUID
    is_active: bool

    def get_id(self) -> UUID:
        """Return the session ID."""
        ...


@dataclass(slots=True)
class PermissionGroupDto:
    """Data transfer object for permission group."""

    name: str
    system_key: str | None


@dataclass(slots=True)
class UserDto:
    """Data transfer object for user.

    Implements Flask-Login interface via composition instead of inheritance.
    """

    id: UUID
    email: str

    first_name: str | None
    last_name: str | None

    sex: str

    session: SessionDto | None = None
    permissions: frozenset[tuple[str, str]] = field(default_factory=frozenset)
    permission_groups: tuple[PermissionGroupDto, ...] = field(default_factory=tuple)

    def get_id(self) -> UUID | None:
        """Return the session ID for Flask-Login compatibility."""
        return self.session.id if self.session else None

    @property
    def is_active(self) -> bool:
        """Check if user session is active."""
        return self.session.is_active if self.session else False

    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated (has active session)."""
        return self.session is not None and self.session.is_active

    @property
    def is_anonymous(self) -> bool:
        """Check if user is anonymous (no active session)."""
        return self.session is None or not self.session.is_active

    @property
    def created_at(self) -> datetime:
        """Extract creation timestamp from UUID."""
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
