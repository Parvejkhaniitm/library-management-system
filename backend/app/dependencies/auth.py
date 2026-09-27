# Depends — FastAPI ka dependency injection system
# HTTPException — error response bhejne ke liye
# status — HTTP status codes (401, 403, etc.) ke readable names
from fastapi import Depends, HTTPException, status

# Cookie se ya header se token nikalne ke liye
from fastapi.security import OAuth2PasswordBearer

# Session — database se baat karne ke liye
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole


# Yeh batata hai FastAPI ko ki token kahan se milega
# tokenUrl sirf documentation (Swagger UI) ke liye use hota hai
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Yeh dependency har protected route mein use hogi.
    Kaam:
    1. Request se access token nikalta hai (Authorization header se)
    2. Token ko decode karta hai
    3. Token se user_id nikal ke database se real User dhoondta hai
    4. Agar kuch bhi galat hai (token invalid, user nahi mila, inactive hai)
       -> 401 Unauthorized error deta hai
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    # Agar token bheja hi nahi gaya
    if token is None:
        raise credentials_error

    try:
        payload = decode_token(token)
    except ValueError:
        # decode_token humne pehle banaya tha - agar token invalid/expired
        # hai to yeh ValueError raise karta hai
        raise credentials_error

    # Sirf "access" type token yahan accept karenge, refresh token nahi
    if payload.get("type") != "access":
        raise credentials_error

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error

    # Database se real user dhoondo
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_error

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive"
        )

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Yeh dependency sirf admin-only routes mein use hogi.
    Pehle get_current_user chalega (login check), fir yeh
    role check karega.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_student(current_user: User = Depends(get_current_user)) -> User:
    """
    Yeh dependency sirf student-only routes mein use hogi.
    """
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required"
        )
    return current_user