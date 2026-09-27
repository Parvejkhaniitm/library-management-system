from sqlalchemy import Column, Integer, Numeric, Date, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class LockerAssignmentStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"
    CANCELLED = "CANCELLED"


class LockerAssignment(Base):
    __tablename__ = "locker_assignments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    locker_id = Column(Integer, ForeignKey("lockers.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    # Locker ka monthly fee 'snapshot' - jaise membership mein hourly_rate_snapshot
    monthly_fee_snapshot = Column(Numeric(10, 2), nullable=False)

    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(Enum(LockerAssignmentStatus), default=LockerAssignmentStatus.ACTIVE, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
