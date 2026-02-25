from typing import Literal
from uuid import UUID

from app.backend.converters.user_converter import UserConverter
from app.backend.database.models import User
from app.backend.domain import UserDto
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.auth.auth_service import AuthService
from app.backend.services.base import BaseService, SqlService
from app.backend.services.session.session_service import SessionService


class UserService(BaseService):
    """Service for managing users"""

    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository(SqlService(model=User))
        self.auth_service = AuthService()
        self.session_service = SessionService()

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        sex: Literal["MALE", "FEMALE", "NOT_SPECIFIED"] = "NOT_SPECIFIED",
    ) -> UserDto | None:
        """Create new user"""
        try:
            user = self.user_repo.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                sex=sex,
            )
            return UserConverter.to_dto(user)
        except ValueError:
            return None

    def get_user(self, user_id: UUID) -> UserDto | None:
        """Get user by ID"""
        user = self.user_repo.get_by_id(user_id)
        return UserConverter.to_dto(user)

    def update_user(
        self,
        user_id: UUID,
        first_name: str,
        last_name: str,
        sex: str,
        password: str | None = None,
    ) -> UserDto | None:
        """Update user"""
        user = self.user_repo.update_user(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            password=password,
        )
        return UserConverter.to_dto(user)

    def check_email_available(self, email: str) -> bool:
        """Check email availability"""
        return self.auth_service.check_email_available(email)

    def authenticate(
        self,
        email: str,
        password: str,
        ip: str | None = None,
        os: str | None = None,
        browser: str | None = None,
    ) -> UserDto | None:
        """Authenticate user"""
        return self.auth_service.authenticate(
            email=email,
            password=password,
            ip=ip,
            os=os,
            browser=browser,
        )

    def get_user_by_session(self, session_id: UUID) -> UserDto | None:
        """Get user by session ID"""
        return self.session_service.get_user_by_session(session_id)

    def create_session(
        self,
        user: UserDto | User,
        ip: str | None,
        os: str | None = None,
        browser: str | None = None,
    ) -> UserDto:
        """Create session for user"""
        return self.session_service.create_session(
            user=user,
            ip=ip,
            os=os,
            browser=browser,
        )

    def deactivate_session(self, session_id: UUID) -> bool:
        """Deactivate session"""
        return self.session_service.deactivate_session(session_id)

    def get_active_sessions(self, user_id: UUID, exclude_id: UUID | None = None):
        """Get user's active sessions"""
        return self.session_service.get_active_sessions(user_id, exclude_id)
