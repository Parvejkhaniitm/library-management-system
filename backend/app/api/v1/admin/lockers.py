from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.locker import LockerCreateRequest, LockerResponse
from app.services.locker_service import create_locker, list_lockers
from app.dependencies.auth import require_admin

router = APIRouter(
    prefix="/api/v1/admin/lockers",
    tags=["admin - lockers"],
    dependencies=[Depends(require_admin)]
)


@router.post("", response_model=LockerResponse, status_code=201)
def admin_create_locker(data: LockerCreateRequest, db: Session = Depends(get_db)):
    return create_locker(db, data)


@router.get("", response_model=list[LockerResponse])
def admin_list_lockers(db: Session = Depends(get_db)):
    return list_lockers(db)
