from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.seat import Seat
from app.models.room import Room
from app.schemas.seat import SeatCreateRequest


def create_seat(db: Session, room_id: int, data: SeatCreateRequest) -> Seat:
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    existing_seat = db.query(Seat).filter(
        Seat.room_id == room_id,
        Seat.seat_number == data.seat_number
    ).first()
    if existing_seat is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A seat with this number already exists in this room"
        )

    new_seat = Seat(room_id=room_id, seat_number=data.seat_number)
    db.add(new_seat)
    db.commit()
    db.refresh(new_seat)
    return new_seat


def list_seats_by_room(db: Session, room_id: int) -> list[Seat]:
    return db.query(Seat).filter(Seat.room_id == room_id).all()


def list_available_seats(db: Session, room_id: int = None) -> list[Seat]:
    query = db.query(Seat).filter(Seat.status == "AVAILABLE")
    if room_id is not None:
        query = query.filter(Seat.room_id == room_id)
    return query.all()
