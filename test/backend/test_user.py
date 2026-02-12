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


def test_session(backend: Backend, user: UserTest):
    user_dto = backend.user.auth(email=user.email, password=user.pwd)
    user_with_session = backend.user.create_session(
        user=user_dto, ip="0.0.0.0", os="LINUX"
    )
    assert user_with_session is not None
    assert user_with_session.session is not None
    assert user_with_session.id == user_dto.id

    user_dto_from_session = backend.user.get_user_by_session(
        session_id=user_with_session.session.id
    )
    assert user_dto_from_session.id == user_dto.id

    backend.user.deactivate_session(session_id=user_with_session.session.id)

    user_dto_from_deactivate_session = backend.user.get_user_by_session(
        session_id=user_with_session.session.id
    )
    assert user_dto_from_deactivate_session is None


def test_update(backend: Backend, user: UserTest):
    user_dto = backend.user.auth(email=user.email, password=user.pwd)
    assert user_dto is not None

    update_user = backend.user.update_user(
        user_id=user_dto.id,
        first_name="Test Update",
        last_name="Test Update",
        sex="FEMALE",
        password="123",
    )
    assert update_user is not None
    assert update_user.first_name == "Test Update"

    user_dto = backend.user.auth(email=user.email, password=user.pwd)
    assert user_dto is None

    user_dto = backend.user.auth(email=user.email, password="123")
    assert user_dto is not None
    assert user_dto.first_name == "Test Update"
    assert user_dto.last_name == "Test Update"
    assert user_dto.sex == "FEMALE"

    update_user = backend.user.update_user(
        user_id=user_dto.id,
        first_name="Test",
        last_name="Test",
        sex="FEMALE",
        password=user.pwd,
    )
    assert update_user is not None
