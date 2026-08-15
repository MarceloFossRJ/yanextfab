from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: Literal["development", "production", "test"] = "development"

    database_url: str = "postgresql+asyncpg://yanextfab:yanextfab@localhost:5432/yanextfab"

    jwt_secret: str = "dev-secret-change-me-before-deploying-anywhere-real"
    jwt_lifetime_seconds: int = 3600

    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_from: str = "noreply@yanextfab.dev"
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_tls: bool = False
    smtp_ssl: bool = False

    frontend_url: str = "http://localhost:3000"

    anthropic_api_key: str | None = None
    # "provider:model", passed to langchain's init_chat_model — change this to swap providers
    # without touching agent code. See design.md's AI-agent decision.
    llm_model: str = "anthropic:claude-sonnet-5"

    openapi_export_path: str | None = None

    @property
    def psycopg_database_url(self) -> str:
        """The same database, in the plain `postgresql://` DSN form psycopg (used by the
        LangGraph checkpointer) expects, rather than SQLAlchemy's `postgresql+asyncpg://`."""
        return self.database_url.replace("postgresql+asyncpg://", "postgresql://")


@lru_cache
def get_settings() -> Settings:
    return Settings()
