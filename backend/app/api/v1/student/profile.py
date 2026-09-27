from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.student import StudentMeResponse
from app.services.student_service import get_own_profile
from app.dependencies.auth import require_student
from app.models.user import User

router = APIRouter(prefix="/api/v1/student", tags=["student"])


@router.get("/profile", response_model=StudentMeResponse)
def get_my_profile(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Logged-in student apni profile dekhta hai. current_user JWT token
    se aata hai — student koi ID nahi bhej sakta, isliye sirf apna
    data hi dekh sakta hai.
    """
    profile = get_own_profile(db, current_user.id)

    # StudentMeResponse ko dono jagah se data chahiye (User se email,
    # StudentProfile se baaki sab) — isliye hum manually dict banate hain
    return StudentMeResponse(
        id=profile.id,
        student_code=profile.student_code,
        full_name=profile.full_name,
        email=current_user.email,
        phone=profile.phone,
        whatsapp_number=profile.whatsapp_number,
        email_notifications_enabled=profile.email_notifications_enabled,
        whatsapp_notifications_enabled=profile.whatsapp_notifications_enabled,
        status=profile.status.value,
    )