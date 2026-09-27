from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.room import RoomCreateRequest, RoomResponse
from app.schemas.seat import SeatCreateRequest, SeatResponse
from app.services.room_service import create_room, list_rooms, get_room_by_id
from app.services.seat_service import create_seat, list_seats_by_room
from app.dependencies.auth import require_admin

router = APIRouter(
    prefix="/api/v1/admin/rooms",
    tags=["admin - rooms"],
    dependencies=[Depends(require_admin)]
)


@router.post("", response_model=RoomResponse, status_code=201)
def admin_create_room(data: RoomCreateRequest, db: Session = Depends(get_db)):
    """Naya room banata hai."""
    return create_room(db, data)


@router.get("", response_model=list[RoomResponse])
def admin_list_rooms(db: Session = Depends(get_db)):
    """Saare rooms ki list."""
    return list_rooms(db)


@router.get("/{room_id}", response_model=RoomResponse)
def admin_get_room(room_id: int, db: Session = Depends(get_db)):
    """Ek specific room ki details."""
    return get_room_by_id(db, room_id)


@router.post("/{room_id}/seats", response_model=SeatResponse, status_code=201)
def admin_create_seat(room_id: int, data: SeatCreateRequest, db: Session = Depends(get_db)):
    """
    Kisi room ke andar naya seat banata hai.
    URL mein room_id path parameter hai — jaise /admin/rooms/1/seats
    """
    return create_seat(db, room_id, data)


@router.get("/{room_id}/seats", response_model=list[SeatResponse])
def admin_list_seats(room_id: int, db: Session = Depends(get_db)):
    """Ek room ki saari seats ki list."""
    return list_seats_by_room(db, room_id)