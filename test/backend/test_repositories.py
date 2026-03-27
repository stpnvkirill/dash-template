"""Tests for repository classes."""

import pytest

from app.backend.database.models import User, UserSession
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.session_repository import SessionRepository
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.session.session_service import SessionService
from test.conftest import UserTest


class TestUserRepository:
    """Tests for UserRepository."""

    @pytest.fixture
    def user_repo(self) -> UserRepository:
        """Fixture for UserRepository."""
        return UserRepository(SqlService(model=User))

    def test_create_user(self, user_repo: UserRepository, user: UserTest) -> None:
        """Test user creation."""
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        assert created_user is not None
        assert created_user.email == user.email
        assert created_user.first_name == "Test"
        assert created_user.last_name == "Test"
        assert created_user.sex.value == "MALE"

    def test_is_email_available(
        self, user_repo: UserRepository, user: UserTest
    ) -> None:
        """Test email availability check."""
        # Email should be available
        assert user_repo.is_email_available(user.email)

        # Create user
        user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Email should no longer be available
        assert not user_repo.is_email_available(user.email)

    def test_get_by_email(self, user_repo: UserRepository, user: UserTest) -> None:
        """Test get user by email."""
        # Create user
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Find user by email
        found_user = user_repo.get_by_email(user.email)
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == user.email

    def test_update_user(self, user_repo: UserRepository, user: UserTest) -> None:
        """Test user update."""
        # Create user
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Update user
        updated_user = user_repo.update_user(
            user_id=created_user.id,
            first_name="Updated",
            last_name="Updated",
            sex="FEMALE",
            password="new_password",
        )

        assert updated_user is not None
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Updated"
        assert updated_user.sex.value == "FEMALE"


class TestSessionRepository:
    """Tests for SessionRepository."""

    @pytest.fixture
    def session_repo(self) -> SessionRepository:
        """Fixture for SessionRepository."""
        return SessionRepository(SqlService(model=UserSession))

    def test_create_and_get_session(
        self, session_repo: SessionRepository, user: UserTest
    ) -> None:
        """Test session creation and retrieval."""
        # Create user
        user_repo = UserRepository(SqlService(model=User))
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="User",
            sex="MALE",
        )

        session_service = SessionService()
        user_dto = session_service.create_session(
            user=created_user, ip="127.0.0.1", os="Linux", browser="Chrome"
        )

        # Get session by ID
        retrieved = session_repo.get_by_id(user_dto.session.id)
        assert retrieved is not None
        assert retrieved.id == user_dto.session.id
        assert str(retrieved.ip_address) == "127.0.0.1"

    def test_deactivate_session(
        self, session_repo: SessionRepository, user: UserTest
    ) -> None:
        """Test session deactivation."""
        user_repo = UserRepository(SqlService(model=User))
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="User",
            sex="MALE",
        )

        session_service = SessionService()
        user_dto = session_service.create_session(
            user=created_user, ip="127.0.0.1", os="Linux", browser="Chrome"
        )

        # Deactivate session
        result = session_repo.deactivate_session(user_dto.session.id)
        assert result is not None
        assert result.is_active is False
