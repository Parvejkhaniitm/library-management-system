from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
)
from app.core.config import settings


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Email + password check karta hai database se.
    Agar match nahi hua, ya user inactive hai -> error raise karta hai.
    """
    user = db.query(User).filter(User.email == email).first()

    # Dhyan de: hum yahan generic error dete hain ("incorrect email or password")
    # specific error nahi ("email nahi mila" ya "password galat hai") —
    # isse attacker ko pata nahi chalega ki email exist karta hai ya nahi.
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive"
        )

    return user


def create_tokens_for_user(db: Session, user: User) -> tuple[str, str]:
    """
    User ke liye naya access token + refresh token banata hai.
    Refresh token ka HASH database mein save karta hai (raw token nahi),
    taaki agar database leak ho, tokens seedha use na ho sakein.
    """
    access_token = create_access_token(user.id, user.role.value)
    refresh_token = create_refresh_token(user.id)

    # Refresh token ka hash store karna hai — hum wahi hashing function
    # use kar rahe hain jo password ke liye banaya tha (yeh generic hai)
    token_hash = hash_password(refresh_token)

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    db_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()

    return access_token, refresh_token


def rotate_refresh_token(db: Session, old_refresh_token: str) -> tuple[str, str]:
    """
    Purane refresh token ko verify karta hai, use "revoke" (cancel) karta hai,
    aur naya access + refresh token pair banata hai.

    Yeh "rotation" security best-practice hai — har refresh pe naya
    refresh token milta hai, purana kaam nahi karega.
    """
    try:
        payload = decode_token(old_refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = int(payload.get("sub"))

    # Database mein saare non-revoked tokens is user ke check karo
    # aur dekho kaunsa match karta hai (hash compare karke)
    candidate_tokens = db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None)
    ).all()

    matched_token = None
    for token_row in candidate_tokens:
        if verify_password(old_refresh_token, token_row.token_hash):
            matched_token = token_row
            break

    if matched_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not recognized or already used"
        )

    # Purane token ko revoke (cancel) kar do
    matched_token.revoked_at = datetime.now(timezone.utc)
    db.commit()

    # User ko fresh se fetch karo (naya token banane ke liye role chahiye)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return create_tokens_for_user(db, user)


def revoke_all_user_tokens(db: Session, user_id: int, raw_refresh_token: str) -> None:
    """
    Logout ke waqt call hota hai — matching refresh token ko revoke karta hai.
    """
    candidate_tokens = db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None)
    ).all()

    for token_row in candidate_tokens:
        if verify_password(raw_refresh_token, token_row.token_hash):
            token_row.revoked_at = datetime.now(timezone.utc)
            db.commit()
            break