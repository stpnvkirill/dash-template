"""Tests for UserService."""

from test.conftest import UserTest


def test_create_user(user_service, user: UserTest) -> None:
    first_check_email = user_service.check_email_available(email=user.email)
    assert first_check_email

    user_dto = user_service.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )
    assert user_dto is not None

    assert user_dto.email == user.email
    get_user_dto = user_service.get_user(user_id=user_dto.id)

    assert get_user_dto is not None
    assert get_user_dto == user_dto


def test_check_email(user_service, user: UserTest) -> None:
    # First, create a user
    user_service.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )

    # Now check that email is not available
    email_available = user_service.check_email_available(email=user.email)
    assert not email_available


def test_authenticate(user_service, user: UserTest) -> None:
    # Create user if it doesn't exist yet
    user_dto = user_service.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )
    assert user_dto is not None

    # Now authenticate
    auth_user_dto = user_service.authenticate(
        email=user.email, password=user.pwd, ip="0.0.0.0", os=None, browser=None
    )
    assert auth_user_dto is not None
    assert auth_user_dto.email == user.email


def test_second_create_user(user_service, user: UserTest) -> None:
    # First, create a user
    first_user_dto = user_service.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )
    assert first_user_dto is not None

    # Now try to create the same user again
    second_user_dto = user_service.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )
    assert second_user_dto is None


def test_session(user_service, user: UserTest) -> None:
    # Create a user
    user_service.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )

    user_dto = user_service.authenticate(
        email=user.email, password=user.pwd, ip="0.0.0.0", os=None, browser=None
    )
    assert user_dto is not None
    assert user_dto.session is not None

    user_dto_from_session = user_service.get_user_by_session(
        session_id=user_dto.session.id
    )
    assert user_dto_from_session.id == user_dto.id

    user_service.deactivate_session(session_id=user_dto.session.id)

    user_dto_from_deactivate_session = user_service.get_user_by_session(
        session_id=user_dto.session.id
    )
    assert user_dto_from_deactivate_session is None


def test_update(user_service, user: UserTest) -> None:
    # Create a user
    user_service.create_user(
        email=user.email,
        password=user.pwd,
        first_name="Test",
        last_name="Test",
        sex="MALE",
    )

    user_dto = user_service.authenticate(
        email=user.email, password=user.pwd, ip="0.0.0.0", os=None, browser=None
    )
    assert user_dto is not None

    update_user = user_service.update_user(
        user_id=user_dto.id,
        first_name="Test Update",
        last_name="Test Update",
        sex="FEMALE",
        password="123",
    )
    assert update_user is not None
    assert update_user.first_name == "Test Update"

    user_dto = user_service.authenticate(
        email=user.email, password=user.pwd, ip="0.0.0.0", os=None, browser=None
    )
    assert user_dto is None

    user_dto = user_service.authenticate(
        email=user.email, password="123", ip="0.0.0.0", os=None, browser=None
    )
    assert user_dto is not None
    assert user_dto.first_name == "Test Update"
    assert user_dto.last_name == "Test Update"
    assert user_dto.sex == "FEMALE"

    update_user = user_service.update_user(
        user_id=user_dto.id,
        first_name="Test",
        last_name="Test",
        sex="FEMALE",
        password=user.pwd,
    )
    assert update_user is not None
