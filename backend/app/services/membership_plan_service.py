from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.membership_plan import MembershipPlan
from app.schemas.membership_plan import MembershipPlanCreateRequest


def create_membership_plan(db: Session, data: MembershipPlanCreateRequest) -> MembershipPlan:
    existing = db.query(MembershipPlan).filter(MembershipPlan.name == data.name).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A plan with this name already exists"
        )

    new_plan = MembershipPlan(
        name=data.name,
        hourly_rate=data.hourly_rate,
        description=data.description
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan


def list_membership_plans(db: Session) -> list[MembershipPlan]:
    return db.query(MembershipPlan).all()


def get_membership_plan_by_id(db: Session, plan_id: int) -> MembershipPlan:
    plan = db.query(MembershipPlan).filter(MembershipPlan.id == plan_id).first()
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership plan not found")
    return plan
