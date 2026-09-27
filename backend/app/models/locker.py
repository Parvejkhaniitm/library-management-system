from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class LockerStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    MAINTENANCE = "MAINTENANCE"
    INACTIVE = "INACTIVE"


class Locker(Base):
    """
    Har row ek locker hai. room_id nullable hai kyunki lockers
    kisi specific room se bandhe nahi ho sakte (jaise ek alag
    locker room mein rakhe ja sakte hain).
    """
    __tablename__ = "lockers"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # nullable=True — locker kisi room se link ho sakta hai, ya nahi bhi
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)

    locker_number = Column(String, unique=True, nullable=False, index=True)

    status = Column(Enum(LockerStatus), default=LockerStatus.AVAILABLE, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
