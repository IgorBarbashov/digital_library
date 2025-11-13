from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings using pydantic-settings."""

    # Postgres / database
    postgres_user: str = Field("fastapi", alias="POSTGRES_USER")
    postgres_password: str = Field("fastapi_pass", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field("fastapi_db", alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    # App
    port: int = Field(8000, alias="PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def db_dsn(self) -> str:
        """Return a postgres DSN. If DATABASE_URL is provided, use it;
        otherwise compose a DSN from the individual Postgres fields.
        """

        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def alembic_db_dsn(self) -> str:
        """Return a postgres DSN fo Alembic. If DATABASE_URL is provided, use it;
        otherwise compose a DSN from the individual Postgres fields.
        """

        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings.model_validate({})
