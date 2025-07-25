## calculation.py
## IS 601 Module 11
## Evan Garvey

from enum import Enum
from typing import Optional
from uuid import UUID
from app.models.calculation import CalculationType
from app.schemas.user import UserResponse
from pydantic import BaseModel, Field, model_validator, ConfigDict

class CalculationCreate(BaseModel):
    a: float = Field(..., example=5.0)
    b: float = Field(..., example=2.0)
    type: CalculationType

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "a": 10.0,
            "b": 2.0,
            "type": "Divide"
        }
    })

    @model_validator(mode="before")
    @classmethod
    def validate_no_zero_division(cls, values):
        if values.get("type") == CalculationType.DIV and values.get("b") == 0:
            raise ValueError("Cannot divide by zero.")
        return values
    
class CalculationRead(BaseModel):
    id: UUID
    a: float
    b: float
    type: CalculationType
    result: Optional[float]
    user_id: UUID
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)