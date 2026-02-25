from typing import Literal
from uuid import UUID

from werkzeug.security import generate_password_hash

from app.backend.database.models import User
from app.backend.services.base import SqlService

from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for working with users"""

    def __init__(self, sql_service: SqlService):
        super().__init__(sql_service)

    def get_by_email(self, email: str) -> User | None:
        """Get user by email"""
        return self.sql_service.get_by(email=email.lower())

    def is_email_available(self, email: str) -> bool:
        """Check email availability"""
        return not self.get_by_email(email)

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        sex: Literal["MALE", "FEMALE", "NOT_SPECIFIED"] = "NOT_SPECIFIED",
    ) -> User:
        """Create new user"""
        if not self.is_email_available(email):
            msg = "Email already exists"
            raise ValueError(msg)

        hashed_password = generate_password_hash(password, method="pbkdf2")

        return self.create(
            email=email.lower(),
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            password=hashed_password,
        )

    def update_user(
        self,
        user_id: UUID,
        first_name: str,
        last_name: str,
        sex: str,
        password: str | None = None,
    ) -> User:
        """Update user"""
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "sex": sex or "NOT_SPECIFIED",
        }

        if password:
            hashed_password = generate_password_hash(password, method="pbkdf2")
            data["password"] = hashed_password

        return self.update(user_id, **data)
