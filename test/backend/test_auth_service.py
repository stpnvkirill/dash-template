"""Tests for AuthService."""

from test.conftest import UserTest


class TestAuthService:
    """Tests for AuthService"""

    def test_authenticate_success(self, auth_service, user: UserTest):
        """Test successful authentication"""
        # Create user through repository directly
        user_repo = auth_service.user_repo

        # Create user
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )
        assert created_user is not None

        # Authenticate user
        user_dto = auth_service.authenticate(
            email=user.email,
            password=user.pwd,
            ip="127.0.0.1",
            os="Linux",
            browser="Chrome",
        )

        assert user_dto is not None
        assert user_dto.email == user.email
        assert user_dto.first_name == "Test"
        assert user_dto.session is not None

    def test_authenticate_wrong_password(self, auth_service, user: UserTest):
        """Test authentication with wrong password"""
        # Create user
        user_repo = auth_service.user_repo
        user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Try to authenticate with wrong password
        user_dto = auth_service.authenticate(
            email=user.email,
            password="wrong_password",
            ip="127.0.0.1",
            os="Linux",
            browser="Chrome",
        )

        assert user_dto is None

    def test_authenticate_nonexistent_user(self, auth_service):
        """Test authentication of nonexistent user"""
        user_dto = auth_service.authenticate(
            email="nonexistent@test.com",
            password="password",
            ip="127.0.0.1",
            os="Linux",
            browser="Chrome",
        )

        assert user_dto is None

    def test_check_email_available(self, auth_service, user: UserTest):
        """Test checking email availability"""
        # Email should be available before creating user
        assert auth_service.check_email_available(user.email)

        # Create user
        user_repo = auth_service.user_repo
        user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Email should no longer be available
        assert not auth_service.check_email_available(user.email)

    def test_authenticate_with_rate_limiting_disabled(self, user: UserTest):
        """Test authentication works when rate limiting is disabled"""
        from app.backend.database.models import User, UserSession
        from app.backend.infrastructure.database import SqlService
        from app.backend.repositories.session_repository import (
            SessionRepository,
        )
        from app.backend.repositories.user_repository import (
            UserRepository,
        )
        from app.backend.services.auth.auth_service import AuthService
        from app.backend.services.session.session_service import (
            SessionService,
        )

        user_repo = UserRepository(SqlService(model=User))
        session_repo = SessionRepository(SqlService(model=UserSession))
        session_service = SessionService(session_repo=session_repo)

        service_no_rate_limit = AuthService(
            user_repo=user_repo,
            session_service=session_service,
            enable_rate_limiting=False,
        )

        # Rate limiter should be None when disabled
        assert service_no_rate_limit._rate_limiter is None

        # Create user
        user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Authenticate should work without rate limiting
        # Make multiple attempts - should not be blocked
        for _ in range(10):  # More than rate limit
            user_dto = service_no_rate_limit.authenticate(
                email=user.email,
                password=user.pwd,
                ip="127.0.0.1",
                os="Linux",
                browser="Chrome",
            )
            # Should succeed every time (no rate limiting)
            assert user_dto is not None
            assert user_dto.email == user.email
