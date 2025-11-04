"""Factory for the Market Analysis subagent."""
from __future__ import annotations

from deepagents import create_deep_agent
from langgraph.store.memory import InMemoryStore

from deep_trader.agents.research_agent import create_research_agent
from deep_trader.tools.search_tool import internet_search
from deep_trader.utils.agent_config_loader import AgentConfigLoader
from deep_trader.utils.config import get_settings
from deep_trader.utils.langsmith import configure_langsmith_tracing


def create_market_analysis_agent():
    """Instantiate the Market Analysis subagent with its configured tools."""
    settings = get_settings()
    configure_langsmith_tracing(settings)

    loader = AgentConfigLoader("agents/market_analysis_agent_config.yaml")
    model_name = loader.get_model_name()
    instructions = loader.get_instructions()

    store = InMemoryStore()
    research_agent = create_research_agent()

    def deep_research(query: str) -> str:
        """Delegate long-form synthesis to the research agent."""
        result = research_agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        return result["messages"][-1].content

    agent = create_deep_agent(
        model=model_name,
        tools=[internet_search, deep_research],
        system_prompt=instructions,
        store=store,
    )
    return agent
