import os
import uuid
from datetime import time, timedelta
from functools import cache
from pathlib import Path
from urllib import urljoin

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Global project settings"""

    app_title: str = "RandomCoffeeBot"
    description: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # Settings connect to the database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "random_coffee_db"
    DB_HOST: str = "localhost"
    DB_PORT: str = 5432

    @property
    def database_url(self) -> str:
        """Get a link to connect to the database"""
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
