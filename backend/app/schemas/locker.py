from pydantic import BaseModel
from typing import Optional


class LockerCreateRequest(BaseModel):
    locker_number: str
    room_id: Optional[int] = None


class LockerResponse(BaseModel):
    id: int
    locker_number: str
    room_id: Optional[int] = None
    status: str

    model_config = {"from_attributes": True}
