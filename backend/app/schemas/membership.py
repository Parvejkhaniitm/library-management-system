from pydantic import BaseModel
from datetime import date, time
from decimal import Decimal
from typing import Optional


class MembershipCreateRequest(BaseModel):
    """Admin jab student ko membership assign karta hai."""
    student_id: int
    plan_id: int
    start_date: date
    end_date: date
    access_start_time: time
    access_end_time: time


class MembershipResponse(BaseModel):
    id: int
    student_id: int
    plan_id: int
    start_date: date
    end_date: date
    access_start_time: time
    access_end_time: time
    daily_scheduled_hours: Decimal
    hourly_rate_snapshot: Decimal
    status: str

    model_config = {"from_attributes": True}
