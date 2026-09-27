# Column types jo humein table mein chahiye
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
# server_default se database khud current time daal dega
from sqlalchemy.sql import func
import enum

# Humara Base class jo db/base.py mein banaya tha
from app.db.base import Base


class UserRole(str, enum.Enum):
    """
    Yeh Python Enum hai — matlab 'role' field mein sirf yeh 2 values
    allowed hongi, kuch aur nahi. Isse galat data (jaise "Admin " ya "manager")
    database mein nahi jaa sakta.
    """
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"


class User(Base):
    """
    Yeh class 'users' naam ka table banayegi database mein.
    Har User row ek login-capable account hai — admin ya student.
    """

    # __tablename__ batata hai database mein table ka naam kya hoga
    __tablename__ = "users"

    # id — primary key, matlab har row ka unique identifier
    # autoincrement=True matlab har naye row pe apne aap 1, 2, 3... badhta jayega
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # email — unique matlab do users same email se nahi ban sakte
    # index=True se email se search fast hoga (jaise login ke waqt)
    email = Column(String, unique=True, index=True, nullable=False)

    # password_hash — yahan HASHED password store hoga, plain text KABHI nahi
    password_hash = Column(String, nullable=False)

    # role — admin ya student, upar wale Enum se restrict kiya
    role = Column(Enum(UserRole), nullable=False)

    # is_active — agar False hai to yeh user login nahi kar payega
    # default=True matlab naya user by default active hoga
    is_active = Column(Boolean, default=True, nullable=False)

    # created_at — jab row bani thi, wo time apne aap record hoga
    # server_default=func.now() matlab database khud current time bharega
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # updated_at — jab bhi row update hogi, yeh time apne aap change hoga
    # onupdate=func.now() — update hone par naya time set karega
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )