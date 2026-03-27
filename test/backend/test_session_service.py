"""Tests for SessionService."""

from app.backend.database.models import User
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.user_repository import UserRepository
from test.conftest import UserTest


class TestSessionService:
    """Tests for SessionService."""

    def test_create_session(self, session_service, user: UserTest) -> None:
        """Test session creation."""
        # Create user through repository
        user_repo = UserRepository(SqlService(model=User))
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )
        assert created_user is not None

        # Create session
        user_dto = session_service.create_session(
            user=created_user, ip="127.0.0.1", os="Linux", browser="Chrome"
        )

        assert user_dto is not None
        assert user_dto.session is not None
        assert user_dto.session.os == "linux"
        assert user_dto.session.browser == "chrome"
        assert str(user_dto.session.ip) == "127.0.0.1"

    def test_deactivate_session(self, session_service, user: UserTest) -> None:
        """Test session deactivation."""
        # Create user and session
        user_repo = UserRepository(SqlService(model=User))
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        user_dto = session_service.create_session(
            user=created_user, ip="127.0.0.1", os="Linux", browser="Chrome"
        )

        session_id = user_dto.session.id

        # Deactivate session
        result = session_service.deactivate_session(session_id)
        assert result is True

        # Check that session is deactivated
        user_from_session = session_service.get_user_by_session(session_id)
        assert user_from_session is None

    def test_get_user_by_session(self, session_service, user: UserTest) -> None:
        """Test getting user by session."""
        # Create user and session
        user_repo = UserRepository(SqlService(model=User))
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        user_dto = session_service.create_session(
            user=created_user, ip="127.0.0.1", os="Linux", browser="Chrome"
        )

        session_id = user_dto.session.id

        # Get user by session
        retrieved_user = session_service.get_user_by_session(session_id)

        assert retrieved_user is not None
        assert retrieved_user.id == user_dto.id
        assert retrieved_user.session.id == session_id

    def test_get_active_sessions(self, session_service, user: UserTest) -> None:
        """Test getting user's active sessions."""
        # Create user
        user_repo = UserRepository(SqlService(model=User))
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Create multiple sessions
        session1 = session_service.create_session(
            user=created_user, ip="127.0.0.1", os="Linux", browser="Chrome"
        )

        session2 = session_service.create_session(
            user=created_user, ip="127.0.0.2", os="Windows", browser="Firefox"
        )

        # Get active sessions (excluding current)
        active_sessions = session_service.get_active_sessions(
            user_id=created_user.id, exclude_id=session1.session.id, limit=50, offset=0
        )

        assert len(active_sessions) == 1
        assert active_sessions[0].id == session2.session.id
        assert active_sessions[0].os == "windows"
        assert active_sessions[0].browser == "firefox"
