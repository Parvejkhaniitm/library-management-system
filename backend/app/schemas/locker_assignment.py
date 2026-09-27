from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional


class LockerAssignmentCreateRequest(BaseModel):
    locker_id: int
    student_id: int
    start_date: date
    monthly_fee: Decimal


class LockerAssignmentResponse(BaseModel):
    id: int
    locker_id: int
    student_id: int
    start_date: date
    end_date: Optional[date] = None
    monthly_fee_snapshot: Decimal
    status: str

    model_config = {"from_attributes": True}
