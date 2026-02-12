from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from flask_login import UserMixin


@dataclass(slots=True)
class UserDto(UserMixin):
    id: UUID
    email: str

    first_name: str | None
    last_name: str | None

    sex: str

    session: SessionDto | None = None

    def get_id(self):
        return self.session.id

    @property
    def created_at(self) -> datetime:
        timestamp_ms = self.id.int >> 80
        return datetime.fromtimestamp(timestamp_ms / 1000.0, tz=UTC)


@dataclass(slots=True)
class SessionDto:
    id: UUID
    is_active: bool
    os: str
    ip: str
