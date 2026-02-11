from app.backend import Backend
from test.conftest import UserTest


def test_create_user(backend: Backend, user: UserTest):
    first_check_email = backend.user.check_email_is_available(email=user.email)
    assert first_check_email

    user_dto = backend.user.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )
    assert user_dto is not None

    assert user_dto.email == user.email
    get_user_dto = backend.user.get_user(id=user_dto.id)

    assert get_user_dto is not None
    assert get_user_dto == user_dto


def test_check_email(backend: Backend, user: UserTest):
    second_check_email = backend.user.check_email_is_available(email=user.email)
    assert not second_check_email


def test_auth(backend: Backend, user: UserTest):
    user_dto = backend.user.auth(email=user.email, password=user.pwd)
    assert user_dto is not None


def test_second_create_user(backend: Backend, user: UserTest):
    user_dto = backend.user.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )
    assert user_dto is None
