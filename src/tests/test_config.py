import json
import pytest
from logan_iq.core.config import ConfigManager


@pytest.fixture
def config_manager(tmp_path):
    config_file = tmp_path / "test_config.json"
    return ConfigManager(config_file=str(config_file))


def test_load_empty_config(config_manager):
    """Test loading an empty configuration file."""
    config_manager.load()
    assert config_manager.all() == {}


def test_delete_key(config_manager):
    """Test deleting a specific configuration key."""
    config_manager.set("a", 1)
    config_manager.set("b", 2)
    config_manager.delete("a")
    assert config_manager.get("a") is None
    assert config_manager.get("b") == 2


def test_delete_all(config_manager):
    """Test deleting all configuration entries."""
    config_manager.set("x", "y")
    config_manager.set("z", "w")
    config_manager.delete()
    assert config_manager.all() == {}


def test_set_and_get_config(config_manager):
    """Test setting and getting a configuration value."""
    config_manager.set("test_key", "test_value")
    assert config_manager.get("test_key") == "test_value"


def test_save_and_load_config(config_manager):
    """Test saving and loading configuration data."""
    config_manager.set("key1", "value1")
    config_manager.save()

    new_manager = ConfigManager(config_file=config_manager.config_file)
    new_manager.load()
    assert new_manager.get("key1") == "value1"


def test_load_invalid_json(config_manager, monkeypatch):
    """Test loading a configuration file with invalid JSON."""
    invalid_json_path = config_manager.config_file
    with open(invalid_json_path, "w") as f:
        f.write("invalid json")

    config_manager.load()
    assert config_manager.all() == {}
