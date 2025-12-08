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
        "cd2e3243103c310c3b56d18c549dffd9b9f16f9b2e6041007f583bc29d635e13",
        alias="JWT_SECRET_KEY",
    )
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")
    access_token_type: str = "bearer"
    access_token_expire_minutes: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # URLs
    api_base_prefix: str = Field("/api/v1")
    auth_prefix: str = Field("/auth")
    get_token_slug: str = Field("/login")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def db_dsn(self) -> str:
        """Compose a DSN from the individual Postgres fields."""

        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings.model_validate({})
