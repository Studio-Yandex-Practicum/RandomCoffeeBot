from pydantic import AnyUrl, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    database_url: PostgresDsn
    db_engine: str
    db_name: str
    db_host: AnyUrl
    db_port: int
    mattermost_url: HttpUrl
    mattermost_port: int
    mattermost_api_part: str
    bot_token: str
    bot_team: str
    ssl_verify: bool
