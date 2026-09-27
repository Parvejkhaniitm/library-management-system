# SQLAlchemy ka declarative_base — yeh ek "parent class" deta hai
# jisse hamare saare table models (User, Room, Seat, etc.) inherit karenge
from sqlalchemy.orm import declarative_base

# Base class banaya — isko import karke har model file mein use karenge
# jaise: class User(Base): ...
Base = declarative_base()