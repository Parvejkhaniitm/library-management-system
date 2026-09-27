from pydantic import BaseModel
from typing import Optional


class RoomCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class RoomResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: str

    model_config = {"from_attributes": True}
