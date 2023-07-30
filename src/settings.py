from logging import DEBUG
from pathlib import Path

from pydantic import AnyUrl, DirectoryPath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_FOLDER = Path(__file__).parent.parent
(ENV_FILE := ROOT_FOLDER / ".env").touch()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True, env_file=ENV_FILE)
    # database connection configuration
    DB_HOST: AnyUrl = "localhost"
    DB_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    # URL of the resource hosting mattermost server
    MATTERMOST_URL: HttpUrl = "http://localhost"
    # port to connect to mattermost server over
    MATTERMOST_PORT: int = 8065
    # url part of the current API version
    MATTERMOST_API_PATH: str = "/api/v4"
    # a token for mattermost bost
    BOT_TOKEN: str
    # name of the mattermost team
    BOT_TEAM: str
    # use SSL
    SSL_VERIFY: bool = False
    # lower bound of logging events that're going to be logged
    LOG_MIN_ERROR_LEVEL: int = DEBUG
    # default logger name
    LOGGER_NAME: str = "root"
    # the directory to save log files to
    LOG_ROOT: DirectoryPath = ROOT_FOLDER / "logs"
