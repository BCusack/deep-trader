from deep_trader.utils.yaml_loader import load_yaml_config


class AgentConfigLoader:
    def __init__(self, config_path: str):
        self._path = config_path
        self._config = load_yaml_config(config_path)

    def get_model_name(self) -> str:
        model_name = self._config.get("model")
        if not model_name:
            raise ValueError(f"Missing 'model' in {self._path}")
        return model_name

    def get_instructions(self) -> str:
        instructions = self._config.get("instructions")
        if not instructions:
            instructions = self._config.get("instruction")
        if not instructions:
            raise ValueError(f"Missing 'instructions' in {self._path}")
        return instructions

    def get_allowed_bybit_tools(self) -> list[str]:
        value = self._config.get("allowed_bybit_tools")
        if value is None:
            tools_section = self._config.get("tools", {})
            value = tools_section.get("mcp_tool_filter", [])

        if value is None:
            return []
        if not isinstance(value, list):
            raise ValueError(
                f"Expected a list for allowed MCP tools in {self._path}"
            )

        return [str(v) for v in value if str(v).strip()]
