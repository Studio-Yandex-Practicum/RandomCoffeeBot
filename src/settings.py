from pathlib import Path
from typing import ClassVar

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_FOLDER = Path(__file__).resolve().parent.parent
DSN_TEMPLATE = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", case_sensitive=True, env_file=ROOT_FOLDER / ".env" if (ROOT_FOLDER / ".env").exists() else None
    )
    HOST: str = "http://host.docker.internal:8579/"
    # database connection configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    # Mattermost bot settings
    MATTERMOST_URL: str = "http://localhost"
    MATTERMOST_PORT: int = 8065
    MATTERMOST_API_PATH: str = "/api/v4"
    WEBHOOK_HOST_ENABLED: bool = True
    WEBHOOK_HOST_URL: str = "http://localhost"
    WEBHOOK_HOST_PORT: int = 8579
    BOT_TOKEN: str
    BOT_TEAM: str = ""
    SSL_VERIFY: bool = False
    # logging settings
    LOG_FILE_LEVEL: str = "DEBUG"
    LOG_CONSOLE_LEVEL: str = "INFO"
    LOGGER_NAME: str = "root"
    LOG_ROOT: ClassVar[Path] = ROOT_FOLDER / "logs"
    LOG_FILE_SIZE: int = 10 * 2**20
    LOG_FILES_TO_KEEP: int = 5
    # admin settings
    ADMIN_USERNAME: str

    @property
    def database_url(self) -> PostgresDsn:
        """assembles a valid DSN from provided settings"""
        return DSN_TEMPLATE.format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            db_name=self.POSTGRES_DB,
        )
