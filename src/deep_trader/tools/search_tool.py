import re
from functools import lru_cache
from typing import Literal

from tavily import TavilyClient
from tavily.errors import BadRequestError

from deep_trader.utils.config import get_settings


class MissingTavilyApiKey(RuntimeError):
    """Raised when TAVILY_API_KEY is not configured."""


class MissingSearchTerms(ValueError):
    """Raised when a search query lacks descriptive keywords."""


@lru_cache(maxsize=1)
def _get_tavily_client() -> TavilyClient:
    settings = get_settings()
    if not settings.tavily_api_key:
        raise MissingTavilyApiKey(
            "Configure TAVILY_API_KEY in the environment or .env file."
        )
    return TavilyClient(api_key=settings.tavily_api_key)


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search through the Tavily API."""
    client = _get_tavily_client()
    if not _has_search_terms(query):
        raise MissingSearchTerms(
            "Add descriptive keywords alongside any site: filters and try again."
        )

    try:
        return client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )
    except BadRequestError as exc:  # pragma: no cover - relies on external service
        raise ValueError(f"Search failed: {exc}") from exc


def _has_search_terms(query: str) -> bool:
    """Return True when the query contains terms beyond site: filters."""
    if not query or not query.strip():
        return False

    cleaned = re.sub(r"\bsite:[^\s]+\b", "", query, flags=re.IGNORECASE)
    return bool(cleaned.strip())
