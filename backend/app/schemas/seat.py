from pydantic import BaseModel


class SeatCreateRequest(BaseModel):
    seat_number: str


class SeatResponse(BaseModel):
    id: int
    room_id: int
    seat_number: str
    status: str

    model_config = {"from_attributes": True}
