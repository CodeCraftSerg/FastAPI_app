from typing import Any

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://username:password@host:port/db_name"
    SECRET_HASH_KEY: str = "1234567890"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: EmailStr = "user@email.com"
    MAIL_PASSWORD: str = "password"
    MAIL_FROM: str = "user@email.com"
    MAIL_PORT: int = 000
    MAIL_SERVER: str = "smtp.email.com"
    REDIS_DOMAIN: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = "name"
    CLD_API_KEY: int = 000000000000000
    CLD_API_SECRET: str = "secret"

    @field_validator("ALGORITHM")  # noqa
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("Algorithm must be HS256, HS512")
        return v

    model_config = ConfigDict(
        extra="ignore",
        env_file=".env",  # noqa
        env_file_encoding="utf-8",  # noqa
    )


config = Settings()
