import logging
from dataclasses import field
from pathlib import Path
from typing import Optional, Sequence

from pydantic_settings import BaseSettings

ROOT_FOLDER = Path(__file__).parent.parent


class Settings(BaseSettings):
    #    model_config = SettingsConfigDict(
    #        extra="ignore", case_sensitive=True, env_file=ENV_FILE if (ENV_FILE := ROOT_FOLDER / ".env").exists() else None
    #    )
    # database connection configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    # Mattermost bot settings
    MATTERMOST_URL: str = "localhost"
    MATTERMOST_PORT: int = 8065
    MATTERMOST_API_PATH: str = "/api/v4"
    BOT_TOKEN: str = "xzohhrnp5pdiujnizu5x9eqq4r"
    BOT_TEAM: str = "bot"
    IGNORE_USERS: Sequence[str] = field(default_factory=list)
    SSL_VERIFY: bool = False
    WEBHOOK_HOST_ENABLED: bool = False
    SCHEDULER_PERIOD: float = 1.0
    DEBUG: bool = False
    LOG_FORMAT: str = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"
    LOG_DATE_FORMAT: str = "%m/%d/%Y %H:%M:%S"
    LOG_FILE: Optional[str] = None
    SCHEME: str = "http"
    # logging settings
    LOG_MIN_ERROR_LEVEL: int = logging.DEBUG
    LOGGER_NAME: str = "root"
    LOG_ROOT: str = "/logs"
