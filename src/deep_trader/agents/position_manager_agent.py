"""Factory for the Position Manager subagent."""
from __future__ import annotations

from deepagents import create_deep_agent
from langgraph.store.memory import InMemoryStore

from deep_trader.utils.agent_config_loader import AgentConfigLoader
from deep_trader.utils.config import get_settings
from deep_trader.utils.langsmith import configure_langsmith_tracing
from deep_trader.utils.mcp import get_bybit_mcp_tools


def create_position_manager_agent():
    """Instantiate the Position Manager subagent with Bybit MCP tools."""
    settings = get_settings()
    configure_langsmith_tracing(settings)

    loader = AgentConfigLoader("agents/position_manager_agent_config.yaml")
    model_name = loader.get_model_name()
    instructions = loader.get_instructions()
    allowed_tools = loader.get_allowed_bybit_tools()

    tools = get_bybit_mcp_tools(allowed_tools)
    store = InMemoryStore()

    agent = create_deep_agent(
        model=model_name,
        tools=tools,
        system_prompt=instructions,
        store=store,
    )
    return agent
