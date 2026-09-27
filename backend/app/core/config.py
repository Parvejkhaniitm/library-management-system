# pydantic-settings — yeh library .env file ko automatically padh ke
# Python variables mein convert kar deti hai, type-checking ke saath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Yeh class .env file ki har line ko ek Python attribute banayegi

    # JWT token sign/verify karne ke liye secret key
    SECRET_KEY: str

    # Kaunsa encryption algorithm use karna hai JWT ke liye
    ALGORITHM: str = "HS256"

    # Access token kitni jaldi expire hoga (minutes mein)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    # Refresh token kitne din tak valid rahega
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database connect karne ka URL
    DATABASE_URL: str

    # Yeh batata hai ki settings kahan se padhni hain
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Ek single "settings" object banaya jo pura app import karke use karega
settings = Settings()