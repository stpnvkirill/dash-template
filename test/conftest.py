from uuid import uuid4

import pytest

from app.backend import Backend

from .models import UserTest

test_email = f"test_{uuid4()}@test.ru"


@pytest.fixture(scope="function")
def backend():
    yield Backend()


@pytest.fixture(scope="function")
def user():
    """Fixture for test user"""

    unique_email = f"test_{uuid4()}@test.ru"
    return UserTest(email=unique_email, pwd="Qwerty123!")
