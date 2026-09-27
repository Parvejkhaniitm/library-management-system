# BaseModel — Pydantic ka core class, isse hum "shape" define karte hain
# data ka (kaunse fields hain, kaunsa type hai)
from pydantic import BaseModel, EmailStr



class LoginRequest(BaseModel):
    """
    Yeh define karta hai ki login API ko POST request mein
    kya bhejna hoga. EmailStr automatically check karega ki
    yeh valid email format hai ya nahi.
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Login successful hone par yeh response bhejenge.
    Refresh token yahan nahi hai — wo humne HttpOnly cookie mein
    bhejna hai (security ke liye), sirf access_token JSON mein aayega.
    """
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """
    /auth/me endpoint ke liye — current logged-in user ki info.
    Dhyan de: password_hash yahan bilkul NAHI hai — kabhi bhi
    password wapas frontend ko nahi bhejte, even hashed form mein.
    """
    id: int
    email: str
    role: str
    is_active: bool

    # Yeh Pydantic ko batata hai ki yeh data SQLAlchemy model se
    # bhi bana sakta hai (na sirf dict se) — 'ORM mode' enable karta hai
    model_config = {"from_attributes": True}