"""LangSmith tracing utilities."""
from __future__ import annotations

import os
from deep_trader.utils.config import Settings


def configure_langsmith_tracing(settings: Settings) -> None:
    """Enable LangSmith tracing based on settings and validate required fields.

    Sets environment variables expected by LangSmith if ``langsmith_tracing`` is
    truthy. Raises ValueError when required fields are missing.
    """
    if not getattr(settings, "langsmith_tracing", False):
        return

    if not getattr(settings, "langsmith_endpoint", None):
        raise ValueError("LANGSMITH_ENDPOINT is not set in .env or config.py")
    if not getattr(settings, "langsmith_api_key", None):
        raise ValueError("LANGSMITH_API_KEY is not set in .env or config.py")
    if not getattr(settings, "langsmith_project", None):
        raise ValueError("LANGSMITH_PROJECT is not set in .env or config.py")

    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint  # type: ignore[arg-type]
    os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key  # type: ignore[arg-type]
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project  # type: ignore[arg-type]
