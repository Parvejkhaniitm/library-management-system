from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.room import Room
from app.schemas.room import RoomCreateRequest


def create_room(db: Session, data: RoomCreateRequest) -> Room:
    existing = db.query(Room).filter(Room.name == data.name).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A room with this name already exists"
        )

    new_room = Room(name=data.name, description=data.description)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


def list_rooms(db: Session) -> list[Room]:
    return db.query(Room).all()


def get_room_by_id(db: Session, room_id: int) -> Room:
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    return room
