from deepagents import create_deep_agent
from langgraph.store.memory import InMemoryStore

from deep_trader.agents.market_analysis_agent import create_market_analysis_agent
from deep_trader.agents.position_manager_agent import create_position_manager_agent
from deep_trader.utils.config import get_settings
from deep_trader.utils.agent_config_loader import AgentConfigLoader
from deep_trader.utils.langsmith import configure_langsmith_tracing


def create_trader_agent():
    """Create the top-level Trader deep agent that orchestrates subagents."""
    settings = get_settings()
    configure_langsmith_tracing(settings)

    loader = AgentConfigLoader("agents/trader_agent_config.yaml")
    model_name = loader.get_model_name()
    instructions = loader.get_instructions()

    store = InMemoryStore()

    def run_market_analysis(task: str) -> str:
        """Delegate discovery work to the Market Analysis subagent."""
        agent = create_market_analysis_agent()
        result = agent.invoke({
            "messages": [{"role": "user", "content": task}]
        })
        return result["messages"][-1].content

    def manage_position(task: str) -> str:
        """Delegate execution planning to the Position Manager subagent."""
        agent = create_position_manager_agent()
        result = agent.invoke({
            "messages": [{"role": "user", "content": task}]
        })
        return result["messages"][-1].content

    agent = create_deep_agent(
        model=model_name,
        tools=[run_market_analysis, manage_position],
        system_prompt=instructions,
        store=store,
    )
    return agent
