from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.locker_assignment import LockerAssignmentCreateRequest, LockerAssignmentResponse
from app.services.locker_assignment_service import assign_locker, end_locker_assignment
from app.dependencies.auth import require_admin
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/admin/locker-assignments",
    tags=["admin - locker assignments"],
    dependencies=[Depends(require_admin)]
)


@router.post("", response_model=LockerAssignmentResponse, status_code=201)
def admin_assign_locker(
    data: LockerAssignmentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return assign_locker(db, data, current_user.id)


@router.patch("/{assignment_id}/end", response_model=LockerAssignmentResponse)
def admin_end_locker_assignment(assignment_id: int, db: Session = Depends(get_db)):
    return end_locker_assignment(db, assignment_id)
