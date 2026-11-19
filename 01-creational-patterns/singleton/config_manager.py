"""Shared application configuration loaded on first access."""

import json
from copy import deepcopy
from pathlib import Path
from threading import Lock
from typing import Any, ClassVar, Self


_CONFIG_PATH = Path(__file__).with_name("config.json")


class ConfigManager:
    _instance: ClassVar[Self | None] = None
    _lock = Lock()

    def __new__(cls) -> Self:
        with cls._lock:
            if cls._instance is None:
                with _CONFIG_PATH.open(encoding="utf-8") as config_file:
                    config = json.load(config_file)
                if not isinstance(config, dict):
                    raise ValueError("Configuration must be a JSON object")

                instance = super().__new__(cls)
                instance._config = config
                cls._instance = instance
            return cls._instance

    @classmethod
    def get_instance(cls) -> Self:
        return cls()

    def get(self, key: str) -> Any:
        """Return a value addressed by a dotted key, or raise KeyError."""
        value = self._config
        for segment in key.split("."):
            if not segment or not isinstance(value, dict) or segment not in value:
                raise KeyError(key)
            value = value[segment]
        return deepcopy(value)
