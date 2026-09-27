from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.membership import MembershipCreateRequest, MembershipResponse
from app.services.membership_service import create_membership, list_memberships_by_student
from app.dependencies.auth import require_admin
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/admin/memberships",
    tags=["admin - memberships"],
    dependencies=[Depends(require_admin)]
)


@router.post("", response_model=MembershipResponse, status_code=201)
def admin_create_membership(
    data: MembershipCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return create_membership(db, data, current_user.id)


@router.get("/student/{student_id}", response_model=list[MembershipResponse])
def admin_get_student_memberships(student_id: int, db: Session = Depends(get_db)):
    return list_memberships_by_student(db, student_id)
