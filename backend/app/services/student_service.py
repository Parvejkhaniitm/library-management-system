from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.models.student_profile import StudentProfile
from app.core.security import hash_password
from app.schemas.student import StudentCreateRequest
from app.utils.student_code import generate_student_code


def create_student(db: Session, data: StudentCreateRequest) -> StudentProfile:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    new_user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=UserRole.STUDENT,
        is_active=True
    )
    db.add(new_user)
    db.flush()

    student_code = generate_student_code(db)

    new_profile = StudentProfile(
        user_id=new_user.id,
        student_code=student_code,
        full_name=data.full_name,
        phone=data.phone,
        whatsapp_number=data.whatsapp_number,
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


def list_students(db: Session) -> list[StudentProfile]:
    return db.query(StudentProfile).all()


def get_student_by_id(db: Session, student_profile_id: int) -> StudentProfile:
    student = db.query(StudentProfile).filter(StudentProfile.id == student_profile_id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


def get_own_profile(db: Session, user_id: int) -> StudentProfile:
    student = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    return student