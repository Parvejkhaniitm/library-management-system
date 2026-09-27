from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class MembershipPlan(Base):
    """
    Har row ek membership plan hai (jaise 'Basic', 'Premium').
    hourly_rate — is plan ka current rate. Naya membership banane
    ke waqt yeh rate 'snapshot' ke roop mein memberships table
    mein copy hoga, taaki future rate changes purani fees ko
    affect na karein.
    """
    __tablename__ = "membership_plans"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    # Numeric(10, 2) — money ke liye Decimal type, floating point NAHI use karte
    # 10 total digits, 2 decimal places (jaise 9999999.99 tak)
    hourly_rate = Column(Numeric(10, 2), nullable=False)

    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
