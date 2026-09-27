from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class StudentStatus(str, enum.Enum):
    """
    Student ki current situation batata hai library ke saath.
    ACTIVE — normal, sab kuch theek
    INACTIVE — temporarily suspended access nahi (admin ne rok diya)
    SUSPENDED — rule violation ya kisi wajah se block
    LEFT — student ne library chhod di
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    LEFT = "LEFT"


class StudentProfile(Base):
    """
    Har row ek student ki real-world details store karta hai.
    Yeh 'users' table se link hota hai user_id ke through — matlab
    har StudentProfile ka ek matching User (login account) hona zaroori hai.
    """
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # user_id — is student ka login account kaunsa hai (users table se link)
    # unique=True zaroori hai kyunki ek User ka sirf EK StudentProfile ho sakta hai
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # student_code — jaise "STU2026001", library ka apna unique ID system
    student_code = Column(String, unique=True, nullable=False, index=True)

    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    whatsapp_number = Column(String, nullable=True)

    # Notification preferences — student decide karta hai kya reminders chahiye
    email_notifications_enabled = Column(Boolean, default=True, nullable=False)
    whatsapp_notifications_enabled = Column(Boolean, default=True, nullable=False)

    status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())