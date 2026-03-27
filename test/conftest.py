"""Test fixtures and configuration."""

from uuid import uuid4

import pytest

from app.backend.database.models import User, UserSession
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.session_repository import SessionRepository
from app.backend.repositories.user_repository import UserRepository
from app.backend.services.auth.auth_service import AuthService
from app.backend.services.permission.permission_service import PermissionService
from app.backend.services.session.session_service import SessionService
from app.backend.services.user.user_service import UserService

from .models import UserTest


@pytest.fixture(scope="function")
def user_repo():
    """Fixture for UserRepository."""
    return UserRepository(SqlService(model=User))


@pytest.fixture(scope="function")
def session_repo():
    """Fixture for SessionRepository."""
    return SessionRepository(SqlService(model=UserSession))


@pytest.fixture(scope="function")
def permission_service():
    """Fixture for PermissionService."""
    return PermissionService()


@pytest.fixture(scope="function")
def session_service(session_repo, permission_service):
    """Fixture for SessionService with injected dependencies."""
    return SessionService(
        session_repo=session_repo,
        permission_service=permission_service,
    )


@pytest.fixture(scope="function")
def auth_service(user_repo, session_service):
    """Fixture for AuthService with injected dependencies.

    Rate limiting is disabled for tests to avoid flaky tests.
    """
    return AuthService(
        user_repo=user_repo,
        session_service=session_service,
        enable_rate_limiting=False,
    )


@pytest.fixture(scope="function")
def user_service(user_repo, auth_service, session_service):
    """Fixture for UserService with injected dependencies."""
    return UserService(
        user_repo=user_repo,
        auth_service=auth_service,
        session_service=session_service,
    )


@pytest.fixture(scope="function")
def user():
    """Fixture for test user."""
    unique_email = f"test_{uuid4()}@test.ru"
    return UserTest(email=unique_email, pwd="Qwerty123!")
