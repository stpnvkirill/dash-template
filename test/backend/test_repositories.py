import pytest

from app.backend.database.models import User, UserSession
from app.backend.repositories.session_repository import SessionRepository
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.base import SqlService
from app.backend.services.session.session_service import SessionService
from test.conftest import UserTest


class TestUserRepository:
    """Тесты для UserRepository"""

    @pytest.fixture
    def user_repo(self):
        """Фикстура для UserRepository"""
        return UserRepository(SqlService(model=User))

    def test_create_user(self, user_repo, user: UserTest):
        """Тест создания пользователя"""
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

    def test_is_email_available(self, user_repo, user: UserTest):
        """Тест проверки доступности email"""
        # Email должен быть доступен
        assert user_repo.is_email_available(user.email)

        # Создаем пользователя
        user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Email больше не доступен
        assert not user_repo.is_email_available(user.email)

    def test_get_by_email(self, user_repo, user: UserTest):
        """Тест получения пользователя по email"""
        # Создаем пользователя
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Ищем пользователя по email
        found_user = user_repo.get_by_email(user.email)
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == user.email

    def test_update_user(self, user_repo, user: UserTest):
        """Тест обновления пользователя"""
        # Создаем пользователя
        created_user = user_repo.create_user(
            email=user.email,
            password=user.pwd,
            first_name="Test",
            last_name="Test",
            sex="MALE",
        )

        # Обновляем пользователя
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
    """Тесты для SessionRepository"""

    @pytest.fixture
    def session_repo(self):
        """Фикстура для SessionRepository"""
        return SessionRepository(SqlService(model=UserSession))

    def test_create_and_get_session(self, session_repo, user: UserTest):
        """Тест создания и получения сессии"""
        # Создаем пользователя

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

        # Получаем сессию по ID
        retrieved = session_repo.get_by_id(user_dto.session.id)
        assert retrieved is not None
        assert retrieved.id == user_dto.session.id
        assert str(retrieved.ip_address) == "127.0.0.1"

    def test_deactivate_session(self, session_repo, user: UserTest):
        """Тест деактивации сессии"""

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

        # Деактивируем сессию
        result = session_repo.deactivate_session(user_dto.session.id)
        assert result is not None
        assert result.is_active is False
