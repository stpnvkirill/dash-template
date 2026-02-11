from dataclasses import dataclass


@dataclass
class UserDto:
    id: str
    email: str

    first_name: str | None
    last_name: str | None

    sex: str
