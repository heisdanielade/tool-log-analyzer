import json
import os
from typing import Optional

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".logan-iq_config.json")


class ConfigManager:
    """Manage user configuration settings in the home directory.

    The `delete` method accepts an optional `key`. If `key` is provided,
    only that configuration entry is removed. If omitted, the entire
    configuration is cleared.
    """

    def __init__(self, config_file: str = CONFIG_PATH) -> None:
        self.config_file = config_file
        self.config_data = {}
        self.load()

    def load(self) -> dict:
        """Load configuration from the config JSON file. Creates an empty file if it doesn't exist."""
        if not os.path.exists(self.config_file):
            self.config_data = {}
            self.save()
        else:
            with open(self.config_file, "r", encoding="utf-8") as f:
                try:
                    self.config_data = json.load(f)
                except json.JSONDecodeError:
                    self.config_data = {}
        return self.config_data

    def save(self) -> None:
        """Save current configuration to JSON file."""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, indent=4)

    def get(self, key: str, default=None):
        """Get a config value by key."""
        return self.config_data.get(key, default)

    def set(self, key: str, value) -> None:
        """Set a config value."""
        self.config_data[key] = value
        self.save()

    def delete(self, key: Optional[str] = None) -> None:
        """Delete a specific configuration key or all configuration data.

        Args:
            key: If provided, remove only this key. If None, clear all configs.
        """
        if key is None:
            self.config_data.clear()
        else:
            # Remove the key if it exists; do nothing otherwise.
            self.config_data.pop(key, None)
        self.save()

    def all(self) -> dict:
        """Return all configuration data."""
        return self.config_data
