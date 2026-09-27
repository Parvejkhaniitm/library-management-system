from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentCreateRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    whatsapp_number: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    user_id: int
    student_code: str
    full_name: str
    phone: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email_notifications_enabled: bool
    whatsapp_notifications_enabled: bool
    status: str

    model_config = {"from_attributes": True}


class StudentMeResponse(BaseModel):
    """
    Student apna profile dekhne ke liye — StudentResponse jaisa hi hai,
    but isme email bhi add karte hain (jo User table se aata hai,
    StudentProfile table mein nahi hai).
    """
    id: int
    student_code: str
    full_name: str
    email: str
    phone: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email_notifications_enabled: bool
    whatsapp_notifications_enabled: bool
    status: str

    model_config = {"from_attributes": True}