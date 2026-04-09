from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional


class IntakeCreate(BaseModel):
    amount_ml: int = Field(..., gt=0, le=5000, description="Water amount in milliliters (1–5000)")
    note: Optional[str] = Field(None, max_length=200, description="Optional note for this entry")

    @field_validator("amount_ml")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0 ml")
        return v


class IntakeResponse(BaseModel):
    id: int
    amount_ml: int
    note: Optional[str]
    logged_at: datetime

    model_config = {"from_attributes": True}


class DailySummary(BaseModel):
    date: date
    total_ml: int
    entry_count: int
    goal_ml: int
    percentage: float


class AIFeedbackResponse(BaseModel):
    feedback: str
    total_ml: int
