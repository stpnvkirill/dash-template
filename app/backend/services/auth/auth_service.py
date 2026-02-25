from werkzeug.security import check_password_hash

from app.backend.database.models import User
from app.backend.domain import UserDto
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.base import BaseService, SqlService
from app.backend.services.session.session_service import SessionService


class AuthService(BaseService):
    """Service for user authentication"""

    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository(SqlService(model=User))
        self.session_service = SessionService()

    def authenticate(
        self,
        email: str,
        password: str,
        ip: str | None = None,
        os: str | None = None,
        browser: str | None = None,
    ) -> UserDto | None:
        """Authenticate user and create session"""
        user = self.user_repo.get_by_email(email)

        if user and check_password_hash(user.password, password):
            return self.session_service.create_session(
                user=user,
                ip=ip,
                os=os,
                browser=browser,
            )

        return None

    def check_email_available(self, email: str) -> bool:
        """Check email availability"""
        return self.user_repo.is_email_available(email)
