from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.seat import Seat, SeatStatus
from app.models.seat_assignment import SeatAssignment, AssignmentStatus
from app.models.student_profile import StudentProfile
from app.schemas.seat_assignment import SeatAssignmentCreateRequest


def assign_seat(db: Session, data: SeatAssignmentCreateRequest, admin_user_id: int) -> SeatAssignment:
    # Seat exist karti hai aur available hai check karo
    seat = db.query(Seat).filter(Seat.id == data.seat_id).first()
    if seat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seat not found")

    if seat.status != SeatStatus.AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Seat is not available (current status: {seat.status.value})"
        )

    # Student exist karta hai check karo
    student = db.query(StudentProfile).filter(StudentProfile.id == data.student_id).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    # Student ke paas already active assignment to nahi hai
    existing_active = db.query(SeatAssignment).filter(
        SeatAssignment.student_id == data.student_id,
        SeatAssignment.status == AssignmentStatus.ACTIVE
    ).first()
    if existing_active is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This student already has an active seat assignment"
        )

    # Sab checks pass ho gaye - ab assignment banao
    new_assignment = SeatAssignment(
        seat_id=data.seat_id,
        student_id=data.student_id,
        start_date=data.start_date,
        assigned_by=admin_user_id,
        status=AssignmentStatus.ACTIVE
    )
    db.add(new_assignment)

    # Seat ka status update karo - ab yeh OCCUPIED hai
    seat.status = SeatStatus.OCCUPIED

    db.commit()
    db.refresh(new_assignment)
    return new_assignment


def end_seat_assignment(db: Session, assignment_id: int) -> SeatAssignment:
    """
    Assignment ko close karta hai (student ki seat khali karna) -
    end_date set karta hai, status ENDED karta hai, aur seat ko
    wapas AVAILABLE bana deta hai.
    """
    assignment = db.query(SeatAssignment).filter(SeatAssignment.id == assignment_id).first()
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

    if assignment.status != AssignmentStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This assignment is not active"
        )

    assignment.end_date = date.today()
    assignment.status = AssignmentStatus.ENDED

    seat = db.query(Seat).filter(Seat.id == assignment.seat_id).first()
    if seat is not None:
        seat.status = SeatStatus.AVAILABLE

    db.commit()
    db.refresh(assignment)
    return assignment


def list_assignments_by_student(db: Session, student_id: int) -> list[SeatAssignment]:
    """Ek student ki saari assignment history (past + current) deta hai."""
    return db.query(SeatAssignment).filter(
        SeatAssignment.student_id == student_id
    ).order_by(SeatAssignment.start_date.desc()).all()
