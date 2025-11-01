# System prompt to steer the agent to be an expert researcher
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware
from deepagents.middleware.filesystem import FilesystemMiddleware
from langgraph.store.memory import InMemoryStore

from deep_trader.tools.search_tool import internet_search
from deep_trader.utils.yaml_loader import load_yaml_config
from deep_trader.utils.config import get_settings
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


_AGENT_CONFIG = load_yaml_config("agents/research_agent_config.yaml")


def create_research_agent():
    settings = get_settings()

    _configure_langsmith_tracing(settings)

    model_name = _AGENT_CONFIG.get("model")
    instructions = _AGENT_CONFIG.get("instructions")

    if not model_name:
        raise ValueError("Missing 'model' in research_agent_config.yaml")

    if not instructions:
        raise ValueError("Missing 'instructions' in research_agent_config.yaml")

    store = InMemoryStore()

    agent = create_deep_agent(
        model=model_name,
        tools=[internet_search],
        system_prompt=instructions,
        store=store,
    )
    return agent
