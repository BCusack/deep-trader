"""Application configuration loaded from environment variables."""
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


PACKAGE_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = PACKAGE_DIR.parent.parent
ENV_PATHS = [PACKAGE_DIR / ".env", ROOT_DIR / ".env"]


def _first_existing_env() -> str | None:
    for candidate in ENV_PATHS:
        if candidate.is_file():
            return str(candidate)
    return None


class Settings(BaseSettings):
    """Settings model for all environment-driven configuration."""

    tavily_api_key: Optional[str] = None
    langsmith_tracing: Optional[bool] = False
    langsmith_endpoint: Optional[str] = None
    langsmith_api_key: Optional[str] = None
    langsmith_project: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=_first_existing_env(),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached settings instance."""
    return Settings()
