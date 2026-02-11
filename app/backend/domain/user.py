from dataclasses import dataclass


@dataclass(slots=True)
class UserDto:
    id: str
    email: str

    first_name: str | None
    last_name: str | None

    sex: str


@dataclass(slots=True)
class SessionDto:
    id: str
    is_active: bool
    os: str
    ip: str
    user: UserDto
