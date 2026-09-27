from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.seat_assignment import SeatAssignmentCreateRequest, SeatAssignmentResponse
from app.services.seat_assignment_service import assign_seat, end_seat_assignment, list_assignments_by_student
from app.dependencies.auth import require_admin
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/admin/seat-assignments",
    tags=["admin - seat assignments"],
    dependencies=[Depends(require_admin)]
)


@router.post("", response_model=SeatAssignmentResponse, status_code=201)
def admin_assign_seat(
    data: SeatAssignmentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Student ko seat assign karta hai. current_user.id se pata chalta hai
    KAUNSE admin ne yeh assignment ki (audit trail ke liye).
    """
    return assign_seat(db, data, current_user.id)


@router.patch("/{assignment_id}/end", response_model=SeatAssignmentResponse)
def admin_end_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """
    Assignment ko close karta hai — seat khali ho jati hai, wapas
    AVAILABLE ban jati hai.
    """
    return end_seat_assignment(db, assignment_id)


@router.get("/student/{student_id}", response_model=list[SeatAssignmentResponse])
def admin_get_student_assignments(student_id: int, db: Session = Depends(get_db)):
    """Ek student ki poori seat assignment history."""
    return list_assignments_by_student(db, student_id)
