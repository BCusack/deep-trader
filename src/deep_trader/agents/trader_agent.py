from deepagents import create_deep_agent
from langgraph.store.memory import InMemoryStore

from deep_trader.tools.search_tool import internet_search
from deep_trader.utils.config import get_settings
from deep_trader.utils.agent_config_loader import AgentConfigLoader
from deep_trader.agents.research_agent import create_research_agent
import os


def _configure_langsmith_tracing(settings):
    if settings.langsmith_tracing:
        if not settings.langsmith_endpoint:
            raise ValueError("LANGSMITH_ENDPOINT is not set in .env or config.py")
        if not settings.langsmith_api_key:
            raise ValueError("LANGSMITH_API_KEY is not set in .env or config.py")
        if not settings.langsmith_project:
            raise ValueError("LANGSMITH_PROJECT is not set in .env or config.py")

        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
        os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project


def create_trader_agent():
    """Create the top-level crypto Trader deep agent.

    This agent orchestrates research, risk assessment, and planning using tools
    including a nested research agent and internet search.
    """
    settings = get_settings()
    _configure_langsmith_tracing(settings)

    config_loader = AgentConfigLoader("agents/trader_agent_config.yaml")
    model_name = config_loader.get_model_name()
    instructions = config_loader.get_instructions()

    # Child agent: research
    research_agent = create_research_agent()

    def research(query: str) -> str:
        """Perform deeper research using the dedicated research agent."""
        result = research_agent.invoke({
            "messages": [
                {"role": "user", "content": query}
            ]
        })
        return result["messages"][-1].content

    def assess_risk(
        thesis: str,
        volatility: str = "medium",
        risk_budget_pct: float = 1.0,
    ) -> dict:
        """Lightweight risk assessment helper.

        Returns an object with suggested stop loss distance, position sizing notes,
        and monitoring reminders. This is a heuristic placeholder and should be
        replaced with a more rigorous model in production.
        """
        vol_map = {"low": 0.5, "medium": 1.0, "high": 1.5}
        vol_factor = vol_map.get(volatility.lower(), 1.0)

        stop_loss_pct = round(1.0 * vol_factor, 2)  # simplistic heuristic
        suggested_r_multiple = round(2.0 / vol_factor, 2)

        return {
            "summary": "Heuristic risk profile generated.",
            "risk_budget_pct": risk_budget_pct,
            "volatility": volatility,
            "stop_loss_pct": stop_loss_pct,
            "target_rr": suggested_r_multiple,
            "notes": [
                "Keep size within daily risk budget.",
                "Adjust invalidation if thesis changes materially.",
            ],
            "thesis_excerpt": thesis[:400],
        }

    store = InMemoryStore()

    agent = create_deep_agent(
        model=model_name,
        tools=[research, internet_search, assess_risk],
        system_prompt=instructions,
        store=store,
    )
    return agent
