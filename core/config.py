import json
import os


class ConfigManager:
    """Manage user configuration settings."""

    def __init__(self, config_file: str = "config.json") -> None:
        self.config_file = config_file
        self.config_data = {}
        self.load()

    def load(self) -> dict:
        """
        Load configuration from the JSON file.
        Creates an empty file if it does not exist.
        """
        if not os.path.exists(self.config_file):
            self.config_data = {}
            self.save()
        else:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                try:
                    self.config_data = json.load(f)
                except json.JSONDecodeError:
                    self.config_data = {}
        return self.config_data

    def save(self) -> None:
        """Save current configuration to the JSON file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, indent=4)

    def get(self, key: str, default=None) -> None:
        """Get a config value by key."""
        return self.config_data.get(key, default)

    def set(self, key: str, value: str) -> None:
        """Set a config value."""
        self.config_data[key] = value

    def all(self) -> dict:
        """Return all configuration data."""
        return self.config_data
