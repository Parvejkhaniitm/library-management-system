from sqlalchemy import Column, Integer, String, Numeric, Date, Time, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class MembershipStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class Membership(Base):
    """
    Har row batata hai ki kis student ki kaunsi membership hai,
    kab se kab tak, aur roz kitne time access hai.
    """
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("membership_plans.id"), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Access timing - jaise 6:00 AM se 10:00 PM tak
    access_start_time = Column(Time, nullable=False)
    access_end_time = Column(Time, nullable=False)

    # Roz kitne ghante access hai (yeh fee calculation mein use hoga)
    daily_scheduled_hours = Column(Numeric(4, 2), nullable=False)

    # Plan ka rate 'snapshot' - jab membership bani thi tab ka rate
    hourly_rate_snapshot = Column(Numeric(10, 2), nullable=False)

    status = Column(Enum(MembershipStatus), default=MembershipStatus.ACTIVE, nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
