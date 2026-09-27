from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class MembershipPlanCreateRequest(BaseModel):
    name: str
    hourly_rate: Decimal
    description: Optional[str] = None


class MembershipPlanResponse(BaseModel):
    id: int
    name: str
    hourly_rate: Decimal
    description: Optional[str] = None
    is_active: bool

    model_config = {"from_attributes": True}
