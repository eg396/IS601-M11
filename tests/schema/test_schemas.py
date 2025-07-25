## test_schemas.py
## IS 601 Module 11
## Evan Garvey

from datetime import datetime
from uuid import uuid4
from app.models.calculation import CalculationType
from app.schemas.calculation import CalculationCreate, CalculationRead
from app.schemas.user import UserResponse
import pytest
from app.schemas import UserCreate
from pydantic import ValidationError

def test_usercreate_valid():
    data = {
        "email": "test@example.com",
        "password": "SecurePass123",
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser"
    }
    user = UserCreate(**data)
    assert user.email == "test@example.com"
    assert user.password == "SecurePass123"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.username == "testuser"

def test_usercreate_missing_email():
    data = {
        "password": "SecurePass123"
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)

def test_usercreate_invalid_email():
    data = {
        "email": "not-an-email",
        "password": "SecurePass123"
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)

def test_password_too_short():
    data = {
        "email": "test@example.com",
        "password": "Abc1",  # less than 6 chars
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser"
    }
    with pytest.raises(ValueError) as exc_info:
        UserCreate(**data)
    assert "password" in str(exc_info.value).lower()

def test_password_no_uppercase():
    data = {
        "email": "test@example.com",
        "password": "securepass123",  # no uppercase letters
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser"
    }
    with pytest.raises(ValueError) as exc_info:
        UserCreate(**data)
    assert "password" in str(exc_info.value).lower()

def test_password_no_lowercase():
    data = {
        "email": "test@example.com",
        "password": "SECUREPASS123",  # no lowercase letters
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser"
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "password" in str(exc_info.value).lower()

def test_password_no_number():
    data = {
        "email": "test@example.com",
        "password": "SecurePass",  # no numbers
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser"
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "password" in str(exc_info.value).lower()

def test_calculation_create_valid():
    data = {
        "a": 10.0,
        "b": 2.0,
        "type": CalculationType.DIV,
    }
    calc = CalculationCreate(**data)
    assert calc.a == 10.0
    assert calc.b == 2.0
    assert calc.type == CalculationType.DIV

def test_calculation_create_division_by_zero():
    data = {
        "a": 10.0,
        "b": 0.0,
        "type": CalculationType.DIV,
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    assert "Cannot divide by zero" in str(exc_info.value)


def test_calculation_read_with_user():
    user_id = uuid4()
    calc_id = uuid4()
    now = datetime.utcnow()

    user_data = {
        "id": user_id,
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "username": "testuser",
        "is_active": True,
        "is_verified": True,
        "created_at": now,
        "updated_at": now
    }

    user = UserResponse(**user_data)

    calc_data = {
        "id": calc_id,
        "a": 5.0,
        "b": 3.0,
        "type": CalculationType.ADD,  # Adjust if your enum uses other labels
        "result": 8.0,
        "user_id": user_id,
        "user": user
    }

    calc = CalculationRead(**calc_data)

    assert calc.user == user
    assert calc.result == 8.0

def test_calculation_read_without_user():
    calc_id = uuid4()
    user_id = uuid4()
    calc_data = {
        "id": calc_id,
        "a": 5.0,
        "b": 3.0,
        "type": CalculationType.SUB,
        "result": 2.0,
        "user_id": user_id,
        "user": None
    }
    calc_read = CalculationRead.model_validate(calc_data)
    assert calc_read.user is None
    assert calc_read.result == 2.0