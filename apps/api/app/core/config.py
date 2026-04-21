from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="allow"
    )

    POSTGRES_USER: str = "jpastor"
    POSTGRES_PASSWORD: str = "123"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "cms_db"
    
    DATABASE_URL: str = "postgresql+asyncpg://jpastor:123@localhost:5432/cms_db"
    SECRET_KEY: str = "super-secret-jwt-key-change-in-production"
    DEBUG: bool = True
    ENVIRONMENT: str = "local"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
