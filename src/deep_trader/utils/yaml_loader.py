"""Helpers for loading YAML configuration files from the package."""
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import yaml

_BASE_DIR = Path(__file__).resolve().parents[1]


class ConfigLoadError(RuntimeError):
    """Raised when a YAML configuration file cannot be loaded."""


@lru_cache(maxsize=None)
def load_yaml_config(relative_path: str) -> Dict[str, Any]:
    """Load and cache a YAML mapping located under the package root."""
    config_path = (_BASE_DIR / relative_path).resolve()
    if not config_path.is_file():
        raise ConfigLoadError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ConfigLoadError(
            f"Expected mapping data in YAML file: {config_path}"
        )

    return data
