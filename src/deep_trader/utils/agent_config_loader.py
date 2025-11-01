from deep_trader.utils.yaml_loader import load_yaml_config


class AgentConfigLoader:
    def __init__(self, config_path: str):
        self._config = load_yaml_config(config_path)

    def get_model_name(self) -> str:
        model_name = self._config.get("model")
        if not model_name:
            raise ValueError("Missing 'model' in research_agent_config.yaml")
        return model_name

    def get_instructions(self) -> str:
        instructions = self._config.get("instructions")
        if not instructions:
            raise ValueError("Missing 'instructions' in research_agent_config.yaml")
        return instructions
