from datetime import datetime, date, time
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.membership import Membership, MembershipStatus
from app.models.membership_plan import MembershipPlan
from app.models.student_profile import StudentProfile
from app.schemas.membership import MembershipCreateRequest


def calculate_daily_hours(start_time: time, end_time: time) -> Decimal:
    """
    access_start_time aur access_end_time se roz kitne ghante
    access hai, yeh calculate karta hai.

    Hum abhi overnight windows (jaise 10 PM se 6 AM) support nahi
    karte - agar end_time start_time se pehle hai, error dete hain.
    Yeh ek clear business decision hai jo hum project mein likh rahe hain.
    """
    if end_time <= start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Overnight access windows are not supported yet. access_end_time must be after access_start_time."
        )

    # Dono time ko ek hi dummy date pe combine karke, unke beech ka
    # duration nikal rahe hain
    dummy_date = date(2000, 1, 1)
    start_dt = datetime.combine(dummy_date, start_time)
    end_dt = datetime.combine(dummy_date, end_time)

    duration = end_dt - start_dt
    hours = Decimal(duration.total_seconds()) / Decimal(3600)
    return hours.quantize(Decimal("0.01"))  # 2 decimal places tak round


def create_membership(db: Session, data: MembershipCreateRequest, admin_user_id: int) -> Membership:
    # Student exist karta hai check karo
    student = db.query(StudentProfile).filter(StudentProfile.id == data.student_id).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    # Plan exist karta hai aur active hai check karo
    plan = db.query(MembershipPlan).filter(MembershipPlan.id == data.plan_id).first()
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership plan not found")
    if not plan.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This membership plan is not active")

    # Date range valid hai check karo
    if data.end_date < data.start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_date cannot be before start_date")

    # Student ke paas already active membership to nahi hai
    existing_active = db.query(Membership).filter(
        Membership.student_id == data.student_id,
        Membership.status == MembershipStatus.ACTIVE
    ).first()
    if existing_active is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This student already has an active membership"
        )

    daily_hours = calculate_daily_hours(data.access_start_time, data.access_end_time)

    new_membership = Membership(
        student_id=data.student_id,
        plan_id=data.plan_id,
        start_date=data.start_date,
        end_date=data.end_date,
        access_start_time=data.access_start_time,
        access_end_time=data.access_end_time,
        daily_scheduled_hours=daily_hours,
        hourly_rate_snapshot=plan.hourly_rate,  # yahan rate 'snapshot' liya
        created_by=admin_user_id,
        status=MembershipStatus.ACTIVE
    )
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership


def list_memberships_by_student(db: Session, student_id: int) -> list[Membership]:
    return db.query(Membership).filter(Membership.student_id == student_id).all()
