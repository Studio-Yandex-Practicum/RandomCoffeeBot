from logging import DEBUG

from pydantic import AnyUrl, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import ROOT_FOLDER


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True, env_file=ROOT_FOLDER / ".env")
    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    DB_ENGINE: str = "postgresql+asyncpg"
    DB_NAME: str = "postgres"
    DB_HOST: AnyUrl = "localhost"
    DB_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    MATTERMOST_URL: HttpUrl = "http://mattermost"
    MATTERMOST_PORT: int = 8065
    MATTERMOST_API_PATH: str = "/api/v4"
    BOT_TOKEN: str
    BOT_TEAM: str
    SSL_VERIFY: bool = False
    LOG_NAME: str = "log.log"
    LOG_MIN_ERROR_LEVEL: str = DEBUG
    LOGGER_NAME: str = "root"
