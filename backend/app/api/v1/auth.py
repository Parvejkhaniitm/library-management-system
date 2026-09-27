# APIRouter — routes ka group banane ke liye (jaise "/auth" wale saare routes)
# Response — cookie set karne ke liye access chahiye hota hai
# Request — cookie se refresh token nikalne ke liye
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_tokens_for_user,
    rotate_refresh_token,
    revoke_all_user_tokens,
)
from app.dependencies.auth import get_current_user
from app.models.user import User

# prefix — sabhi routes ke aage "/api/v1/auth" automatically lag jayega
# tags — Swagger documentation mein grouping ke liye
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Cookie ka naam jisme refresh token store hoga
REFRESH_COOKIE_NAME = "refresh_token"


def set_refresh_cookie(response: Response, refresh_token: str):
    """
    Refresh token ko HttpOnly cookie mein set karta hai.
    HttpOnly=True matlab JavaScript isse read nahi kar sakta (XSS se bachav).
    """
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=False,       # Development mein False, production mein True (HTTPS zaroori)
        samesite="lax",
        max_age=7 * 24 * 60 * 60,  # 7 din, seconds mein
        path="/api/v1/auth"        # Cookie sirf auth routes ke liye bhejega
    )


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login endpoint.
    1. Email+password verify karta hai
    2. Access + refresh token banata hai
    3. Refresh token ko HttpOnly cookie mein bhejta hai
    4. Access token ko JSON response mein bhejta hai
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    access_token, refresh_token = create_tokens_for_user(db, user)

    set_refresh_cookie(response, refresh_token)

    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Jab access token expire ho jaye, frontend yeh endpoint call karega.
    Cookie se purana refresh token nikalta hai, naya pair banata hai.
    """
    old_refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)

    if old_refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )

    access_token, new_refresh_token = rotate_refresh_token(db, old_refresh_token)

    set_refresh_cookie(response, new_refresh_token)

    return TokenResponse(access_token=access_token)


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Logout endpoint — refresh token ko revoke karta hai aur cookie clear karta hai.
    """
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)

    if refresh_token:
        revoke_all_user_tokens(db, current_user.id, refresh_token)

    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/api/v1/auth")

    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Current logged-in user ki info deta hai.
    Frontend isse call karega yeh check karne ke liye ki user login hai ya nahi,
    aur uska role kya hai (admin/student) — dashboard sahi dikhane ke liye.
    """
    return current_user