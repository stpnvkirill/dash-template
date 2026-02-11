from dataclasses import dataclass


@dataclass(slots=True)
class UserTest:
    email: str
    pwd: str
