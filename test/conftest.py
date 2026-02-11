from uuid import uuid4

import pytest

from app.backend import Backend

from .models import UserTest

test_email = f"test_{uuid4()}@test.ru"


@pytest.fixture(scope="session")
def backend():
    yield Backend()


@pytest.fixture(scope="session")
def user():
    """Фикстура для тестового клиента"""
    return UserTest(email=test_email, pwd="Qwerty123!")
