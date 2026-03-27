"""Repository for user data operations.

This repository handles all database operations related to users.
"""

from typing import Literal
from uuid import UUID

from werkzeug.security import generate_password_hash

from app.backend.database.models import User
from app.backend.infrastructure.database import SqlService

from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for working with users.

    Provides methods for user CRUD operations and email-based queries.
    """

    def __init__(self, sql_service: SqlService):
        """Initialize UserRepository.

        Args:
            sql_service: SqlService instance for database operations.
        """
        super().__init__(sql_service)

    def get_by_email(self, email: str) -> User | None:
        """Get user by email address.

        Args:
            email: User email address (case-insensitive).

        Returns:
            User instance or None if not found.
        """
        return self.sql_service.get_by(email=email.lower())

    def is_email_available(self, email: str) -> bool:
        """Check if email is available for registration.

        Args:
            email: Email address to check.

        Returns:
            True if email is available, False if already registered.
        """
        return not self.get_by_email(email)

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        sex: Literal["MALE", "FEMALE", "NOT_SPECIFIED"] = "NOT_SPECIFIED",
    ) -> User:
        """Create new user account.

        Args:
            email: User email address.
            password: Plain text password (will be hashed).
            first_name: User first name.
            last_name: User last name.
            sex: User sex (default: NOT_SPECIFIED).

        Returns:
            Created User instance.

        Raises:
            ValueError: If email is already registered.
        """
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
        """Update user profile.

        Args:
            user_id: User ID.
            first_name: New first name.
            last_name: New last name.
            sex: New sex value.
            password: New password (optional, will be hashed).

        Returns:
            Updated User instance.
        """
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "sex": sex or "NOT_SPECIFIED",
        }

        if password:
            hashed_password = generate_password_hash(password, method="pbkdf2")
            data["password"] = hashed_password

        return self.update(user_id, **data)
