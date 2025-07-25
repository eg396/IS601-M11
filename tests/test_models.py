import pytest
from datetime import datetime, timedelta
from uuid import UUID
from app.models.user import User
from app.schemas.user import UserResponse, Token
from sqlalchemy.exc import IntegrityError

# Use a test database session fixture for isolation (you need to implement this)
# For example, a pytest fixture that returns a SQLAlchemy session bound to a test DB

def test_password_hash_and_verify():
    password = "securepassword"
    hashed = User.hash_password(password)
    assert hashed != password  # hashed should not equal plain password
    user = User(password=hashed)
    assert user.verify_password(password) is True
    assert user.verify_password("wrongpass") is False

def test_create_and_verify_token():
    user_id = UUID("12345678-1234-5678-1234-567812345678")
    token = User.create_access_token({"sub": str(user_id)}, expires_delta=timedelta(minutes=1))
    assert isinstance(token, str)
    verified_id = User.verify_token(token)
    assert verified_id == user_id

    # Test invalid token returns None
    assert User.verify_token("invalidtoken") is None

def test_register_user(db_session):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "username": "johndoe",
        "password": "Strongpassword1"
    }

    user = User.register(db_session, user_data)
    assert user.id is not None
    assert user.email == user_data["email"]
    assert user.verify_password(user_data["password"])

    # Register with duplicate email/username should raise
    with pytest.raises(ValueError):
        User.register(db_session, user_data)

    # Register with short password should raise
    user_data["password"] = "123"
    with pytest.raises(ValueError):
        User.register(db_session, user_data)

def test_authenticate_user(db_session):
    # First register a user to authenticate
    user_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "username": "janedoe",
        "password": "Password123"
    }
    user = User.register(db_session, user_data)
    db_session.commit()

    # Successful authentication returns token dict
    token_data = User.authenticate(db_session, "janedoe", "Password123")
    assert token_data is not None
    assert "access_token" in token_data
    assert "user" in token_data
    assert token_data["user"]["email"] == "jane@example.com"

    # Authentication fails with wrong password or username
    assert User.authenticate(db_session, "janedoe", "wrongpass") is None
    assert User.authenticate(db_session, "wronguser", "Password123") is None

    # last_login updated on successful auth
    db_session.refresh(user)
    assert user.last_login is not None
    assert isinstance(user.last_login, datetime)

def test_user_repr():
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        username="janedoe",
        password="Hashedpassword1"
    )
    expected = "<User(name=Jane Doe, email=jane@example.com)>"
    assert repr(user) == expected