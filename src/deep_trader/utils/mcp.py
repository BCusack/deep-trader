"""Utilities for constructing MCP toolsets used by agents.

This integrates a Bybit MCP server launched via stdio using:

    uvx bybit-mcp

We use `langchain-mcp-adapters` (recommended for LangChain) when available and
fall back to `langchain_mcp` (older package). If neither is installed, we
gracefully return None so callers can skip MCP tools.
"""
from __future__ import annotations

from typing import Iterable, Optional, Dict, List, Any
import os
import asyncio

from deep_trader.utils.config import get_settings


def build_bybit_env() -> Dict[str, str]:
    """Build environment variables for the Bybit MCP server.

    Pulls API keys from settings if available; otherwise relies on process env.
    """
    settings = get_settings()
    env = dict(os.environ)  # inherit current env

    if settings.bybit_api_key:
        env.setdefault("BYBIT_API_KEY", settings.bybit_api_key)
    if settings.bybit_api_secret:
        env.setdefault("BYBIT_API_SECRET", settings.bybit_api_secret)

    return env


async def load_bybit_mcp_tools(allowed_names: Optional[Iterable[str]] = None) -> List[Any]:
    """Load LangChain tools from the Bybit MCP server via stdio.

    Returns a list of langchain_core.tools.BaseTool-compatible objects.
    If adapters or MCP SDK are not available, returns an empty list.
    """
    try:  # optional dependency
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        from langchain_mcp_adapters.tools import load_mcp_tools
    except Exception:
        return []

    server_params = StdioServerParameters(
        command="uvx",
        args=["bybit-mcp"],
        env=build_bybit_env(),
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)
                tools_list = list(tools or [])
                if allowed_names:
                    allowed = {name for name in allowed_names}
                    tools_list = [t for t in tools_list if getattr(t, "name", None) in allowed]
                return tools_list
    except Exception:
        return []


def get_bybit_mcp_tools(allowed_names: Optional[Iterable[str]] = None) -> List[Any]:
    """Synchronous wrapper around ``load_bybit_mcp_tools``.

    Safe to call at startup to retrieve a list of tools. Returns an empty list
    when unavailable or on error.
    """
    try:
        return asyncio.run(load_bybit_mcp_tools(allowed_names))
    except RuntimeError:
        # If already inside an event loop, create a new one manually
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(load_bybit_mcp_tools(allowed_names))
        finally:
            loop.close()
    except Exception:
        return []
