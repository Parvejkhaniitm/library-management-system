from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class SeatStatus(str, enum.Enum):
    """
    Seat ki current situation:
    AVAILABLE — koi assign nahi, khaali hai
    OCCUPIED — kisi student ko assign hai
    MAINTENANCE — repair mein hai
    INACTIVE — band kar diya gaya
    """
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    MAINTENANCE = "MAINTENANCE"
    INACTIVE = "INACTIVE"


class Seat(Base):
    """
    Har row ek seat hai kisi room ke andar.
    Same seat_number 2 different rooms mein ho sakta hai
    (jaise Room A ki Seat 1, Room B ki Seat 1) — but ek room ke
    andar seat_number unique hona chahiye. Isliye hum
    UniqueConstraint use karte hain (room_id, seat_number) pe,
    single column pe nahi.
    """
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    seat_number = Column(String, nullable=False)

    status = Column(Enum(SeatStatus), default=SeatStatus.AVAILABLE, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Yeh table-level constraint hai: (room_id + seat_number) ka combination
    # unique hona chahiye. Matlab Room 1 mein "A1" sirf ek baar ban sakta hai,
    # but Room 2 mein bhi "A1" naam ki seat ban sakti hai (allowed).
    __table_args__ = (
        UniqueConstraint("room_id", "seat_number", name="uq_room_seat_number"),
    )