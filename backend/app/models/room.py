from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class RoomStatus(str, enum.Enum):
    """
    Room ki current condition:
    ACTIVE — normal use mein hai
    INACTIVE — admin ne band kar diya (temporarily)
    MAINTENANCE — repair/cleaning chal rahi hai
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"


class Room(Base):
    """
    Har row library ka ek room represent karta hai
    (jaise "Reading Hall A", "Silent Zone 2", etc.)
    """
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # name — unique hona chahiye, taaki 2 rooms same naam se na bane
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)

    status = Column(Enum(RoomStatus), default=RoomStatus.ACTIVE, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())