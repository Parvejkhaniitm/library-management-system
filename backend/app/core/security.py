# CryptContext — passlib ki class jo hashing algorithm manage karti hai
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

# Yahan humne "argon2" ko default algorithm set kiya
# schemes=["argon2"] matlab sirf argon2 use hoga hashing ke liye
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Plain text password ko hash mein convert karta hai.
    Yeh function tab call hoga jab naya user banaya ja raha ho,
    ya password change kiya ja raha ho.

    Example:
        hash_password("mypassword123")
        -> "$argon2id$v=19$m=65536,t=3,p=4$....(long scrambled text)...."
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Login ke waqt yeh function check karta hai ki user ne jo password
    type kiya, wo database mein stored hash se match karta hai ya nahi.

    Hum kabhi hash ko "decrypt" nahi karte — hum sirf yeh check karte hain
    ki naya plain password, hash karne par same result deta hai ya nahi.
    """
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(user_id: int, role: str) -> str:
    """
    Access token banata hai — isme user ka ID aur role encode hota hai.
    'sub' (subject) = user ki identity, 'role' = admin ya student,
    'exp' = kab expire hoga, 'type' = batata hai ki yeh access token hai
    (refresh token se differentiate karne ke liye).
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
        "type": "access"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    """
    Refresh token banata hai — isme sirf user ID hota hai (role nahi,
    kyunki isse sirf naya access token lene ke liye use karenge, kisi
    protected route ko access karne ke liye nahi).
    """
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Kisi bhi token (access ya refresh) ko decode karke uska payload
    (sub, role, exp, type) wapas deta hai.

    Agar token expired hai ya tampered/invalid hai, JWTError raise hoga —
    isse hum aage auth dependency mein "catch" karke 401 error denge.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise ValueError("Invalid or expired token")