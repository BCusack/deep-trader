# System prompt to steer the agent to be an expert researcher
from deepagents import create_deep_agent

from deep_trader.tools.search_tool import internet_search
from deep_trader.utils.yaml_loader import load_yaml_config


_AGENT_CONFIG = load_yaml_config("agents/research_agent_config.yaml")


def create_research_agent():
    model_name = _AGENT_CONFIG.get("model")
    instructions = _AGENT_CONFIG.get("instructions")

    if not model_name:
        raise ValueError("Missing 'model' in research_agent_config.yaml")

    if not instructions:
        raise ValueError("Missing 'instructions' in research_agent_config.yaml")

    agent = create_deep_agent(
        model=model_name,
        tools=[internet_search],
        system_prompt=instructions,
    )
    return agent
