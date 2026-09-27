from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.student import StudentCreateRequest, StudentResponse
from app.services.student_service import create_student, list_students, get_student_by_id
from app.dependencies.auth import require_admin
from app.models.user import User

# Yeh saare routes sirf admin access kar sakega — require_admin dependency
# poore router pe lagayi hai, taaki har route pe alag se likhna na pade
router = APIRouter(
    prefix="/api/v1/admin/students",
    tags=["admin - students"],
    dependencies=[Depends(require_admin)]
)


@router.post("", response_model=StudentResponse, status_code=201)
def admit_student(
    data: StudentCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Naya student admission karta hai (User + StudentProfile dono banata hai).
    Sirf Admin call kar sakta hai (require_admin dependency check karega).
    """
    return create_student(db, data)


@router.get("", response_model=list[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    """
    Saare students ki list deta hai — admin dashboard ke liye.
    """
    return list_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Ek specific student ki details deta hai, ID se.
    """
    return get_student_by_id(db, student_id)