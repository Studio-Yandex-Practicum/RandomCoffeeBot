POSTGRES_USER: str
POSTGRES_PASSWORD: str
POSTGRES_DB: str = "random_coffee_db"
DB_HOST: str = "localhost"
DB_PORT: str = 5432
TESTING: bool = False


class Settings:
    """Global project settings."""

    @property
    def database_url(self) -> str:
        """Get a link to connect to the database."""
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
