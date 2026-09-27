from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class RefreshToken(Base):
    """
    Har row ek refresh token ko represent karta hai jo kisi user ko
    login ke time diya gaya tha. Hum raw token store nahi karte —
    uska HASH store karte hain (security ke liye), jaise password.
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # ForeignKey — yeh batata hai ki yeh token kis 'user' se belong karta hai
    # ondelete="CASCADE" matlab agar user delete ho, to uske saare tokens bhi delete ho jayenge
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # token_hash — raw token nahi, uska hash store karte hain
    token_hash = Column(String, nullable=False, index=True)

    # expires_at — yeh token kab expire hoga
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # revoked_at — agar yeh field NULL hai, token abhi valid hai
    # agar isme koi time hai, matlab token cancel (logout) ho gaya
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())