from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.membership_plan import MembershipPlanCreateRequest, MembershipPlanResponse
from app.services.membership_plan_service import create_membership_plan, list_membership_plans, get_membership_plan_by_id
from app.dependencies.auth import require_admin

router = APIRouter(
    prefix="/api/v1/admin/membership-plans",
    tags=["admin - membership plans"],
    dependencies=[Depends(require_admin)]
)


@router.post("", response_model=MembershipPlanResponse, status_code=201)
def admin_create_plan(data: MembershipPlanCreateRequest, db: Session = Depends(get_db)):
    return create_membership_plan(db, data)


@router.get("", response_model=list[MembershipPlanResponse])
def admin_list_plans(db: Session = Depends(get_db)):
    return list_membership_plans(db)


@router.get("/{plan_id}", response_model=MembershipPlanResponse)
def admin_get_plan(plan_id: int, db: Session = Depends(get_db)):
    return get_membership_plan_by_id(db, plan_id)
