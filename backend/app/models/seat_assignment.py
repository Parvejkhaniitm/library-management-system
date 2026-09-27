from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class AssignmentStatus(str, enum.Enum):
    """
    ACTIVE — abhi yeh assignment chal raha hai
    ENDED — khatam ho gaya (naturally ya transfer ke wajah se)
    CANCELLED — admin ne cancel kar diya
    """
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"
    CANCELLED = "CANCELLED"


class SeatAssignment(Base):
    """
    Har row ek "student ko seat kab tak assign thi" ka record hai.
    Naya assignment banane ka matlab naya row — purane rows delete
    nahi karte, isse poori history bani rehti hai.
    """
    __tablename__ = "seat_assignments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)

    start_date = Column(Date, nullable=False)
    # end_date NULL matlab abhi bhi active hai (koi end date set nahi hui)
    end_date = Column(Date, nullable=True)

    # assigned_by — kaunse admin (User.id) ne yeh assignment ki
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(Enum(AssignmentStatus), default=AssignmentStatus.ACTIVE, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())