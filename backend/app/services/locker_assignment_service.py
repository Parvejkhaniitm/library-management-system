from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.locker import Locker, LockerStatus
from app.models.locker_assignment import LockerAssignment, LockerAssignmentStatus
from app.models.student_profile import StudentProfile
from app.schemas.locker_assignment import LockerAssignmentCreateRequest


def assign_locker(db: Session, data: LockerAssignmentCreateRequest, admin_user_id: int) -> LockerAssignment:
    locker = db.query(Locker).filter(Locker.id == data.locker_id).first()
    if locker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Locker not found")

    if locker.status != LockerStatus.AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Locker is not available (current status: {locker.status.value})"
        )

    student = db.query(StudentProfile).filter(StudentProfile.id == data.student_id).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    existing_active = db.query(LockerAssignment).filter(
        LockerAssignment.student_id == data.student_id,
        LockerAssignment.status == LockerAssignmentStatus.ACTIVE
    ).first()
    if existing_active is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This student already has an active locker assignment"
        )

    new_assignment = LockerAssignment(
        locker_id=data.locker_id,
        student_id=data.student_id,
        start_date=data.start_date,
        monthly_fee_snapshot=data.monthly_fee,
        assigned_by=admin_user_id,
        status=LockerAssignmentStatus.ACTIVE
    )
    db.add(new_assignment)

    locker.status = LockerStatus.ASSIGNED

    db.commit()
    db.refresh(new_assignment)
    return new_assignment


def end_locker_assignment(db: Session, assignment_id: int) -> LockerAssignment:
    assignment = db.query(LockerAssignment).filter(LockerAssignment.id == assignment_id).first()
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

    if assignment.status != LockerAssignmentStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This assignment is not active")

    assignment.end_date = date.today()
    assignment.status = LockerAssignmentStatus.ENDED

    locker = db.query(Locker).filter(Locker.id == assignment.locker_id).first()
    if locker is not None:
        locker.status = LockerStatus.AVAILABLE

    db.commit()
    db.refresh(assignment)
    return assignment
