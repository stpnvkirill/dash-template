"""Test fixtures and configuration."""

from uuid import uuid4

import pytest

from app.backend.services.factory import ServiceFactory, reset_service_factory

from .models import UserTest


@pytest.fixture(scope="function")
def service_factory():
    """Fixture for service factory."""
    factory = ServiceFactory()
    yield factory
    reset_service_factory()


@pytest.fixture(scope="function")
def user():
    """Fixture for test user."""
    unique_email = f"test_{uuid4()}@test.ru"
    return UserTest(email=unique_email, pwd="Qwerty123!")
