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

    # Auth
    jwt_secret_key: str = Field(
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        alias="JWT_SECRET_KEY",
    )
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")
    access_token_type = "bearer"
    access_token_expire_minutes: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # URLs
    api_base_prefix: str = Field("/api/v1")
    auth_prefix: str = Field("/auth")

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


settings = Settings.model_validate({})
