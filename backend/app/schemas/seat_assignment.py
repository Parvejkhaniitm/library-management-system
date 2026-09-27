from pydantic import BaseModel
from datetime import date
from typing import Optional


class SeatAssignmentCreateRequest(BaseModel):
    seat_id: int
    student_id: int
    start_date: date


class SeatAssignmentResponse(BaseModel):
    id: int
    seat_id: int
    student_id: int
    start_date: date
    end_date: Optional[date] = None
    status: str

    model_config = {"from_attributes": True}
