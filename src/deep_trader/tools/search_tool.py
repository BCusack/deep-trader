from functools import lru_cache
from typing import Literal

from tavily import TavilyClient

from deep_trader.utils.config import get_settings


class MissingTavilyApiKey(RuntimeError):
    """Raised when TAVILY_API_KEY is not configured."""


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
    return client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
