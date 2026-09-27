from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.locker import Locker
from app.schemas.locker import LockerCreateRequest


def create_locker(db: Session, data: LockerCreateRequest) -> Locker:
    existing = db.query(Locker).filter(Locker.locker_number == data.locker_number).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A locker with this number already exists"
        )

    new_locker = Locker(locker_number=data.locker_number, room_id=data.room_id)
    db.add(new_locker)
    db.commit()
    db.refresh(new_locker)
    return new_locker


def list_lockers(db: Session) -> list[Locker]:
    return db.query(Locker).all()
