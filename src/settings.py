from logging import DEBUG
from pathlib import Path

from pydantic import AnyUrl, DirectoryPath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_FOLDER = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=True, env_file=ENV_FILE if (ENV_FILE := ROOT_FOLDER / ".env").exists() else None
    )
    # database connection configuration
    DB_HOST: AnyUrl = "localhost"
    DB_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    # Mattermost bot settings
    MATTERMOST_URL: HttpUrl = "http://localhost"
    MATTERMOST_PORT: int = 8065
    MATTERMOST_API_PATH: str = "/api/v4"
    BOT_TOKEN: str
    BOT_TEAM: str
    SSL_VERIFY: bool = False
    # logging settings
    LOG_MIN_ERROR_LEVEL: int = DEBUG
    LOGGER_NAME: str = "root"
    LOG_ROOT: DirectoryPath = ROOT_FOLDER / "logs"
