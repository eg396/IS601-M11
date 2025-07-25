## calculation.py
## IS 601 Module 11
## Evan Garvey

from sqlalchemy import Column, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
import enum

class CalculationType(str, enum.Enum):
    ADD = "Add"
    SUB = "Sub"
    MUL = "Multiply"
    DIV = "Divide"

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(Enum(CalculationType), nullable=False)
    result = Column(Float, nullable=True)  

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="calculations")