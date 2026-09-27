from sqlalchemy.orm import Session
from app.models.student_profile import StudentProfile


def generate_student_code(db: Session) -> str:
    """
    Database mein abhi tak kitne students hain, unse next number
    calculate karta hai aur "STU00001" jaisa format banata hai.

    Real production mein isse thoda better banaya ja sakta hai
    (jaise year prefix "STU2026001"), but abhi simple rakhte hain.
    """
    count = db.query(StudentProfile).count()
    next_number = count + 1
    return f"STU{next_number:05d}"  # 5 digit padding: STU00001, STU00042, etc.