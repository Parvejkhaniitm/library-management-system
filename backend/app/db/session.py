# create_engine — database ke saath actual connection banata hai
from sqlalchemy import create_engine

# sessionmaker — yeh ek "factory" hai jo har request ke liye
# naya database session (temporary connection) banata hai
from sqlalchemy.orm import sessionmaker

# Humari settings jahan DATABASE_URL rakha hai
from app.core.config import settings

# Engine banaya — yeh SQLite file se actual connection hai
# connect_args sirf SQLite ke liye zaroori hai (multi-thread issue fix karta hai)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal — har API request apna alag session banayega isse
# autocommit=False: matlab hum manually commit() karenge jab data save karna ho
# autoflush=False: matlab SQLAlchemy khud-ba-khud query nahi bhejega jab tak hum na kahein
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Yeh function FastAPI ke 'dependency injection' system ke saath use hoga.
    Har API request pe:
    1. Naya database session banega
    2. Wo session request ko use karne ke liye di jayegi (yield)
    3. Request complete hone ke baad session automatically band ho jayega (finally block)
    Isse hum kabhi bhi database connection "khula" nahi bhoolenge.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()