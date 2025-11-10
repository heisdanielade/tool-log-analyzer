import pytest
from ..logan_iq.core.config import ConfigManager


@pytest.fixture
def config_manager(tmp_path):
    config_file = tmp_path / "test_config.json"
    return ConfigManager(config_file=str(config_file))


def test_load_empty_config(config_manager):
    """Loading an empty configuration file initializes an empty dict."""
    config_manager.load()
    assert config_manager.all() == {}


def test_set_and_get_config(config_manager):
    """Set and retrieve a configuration value."""
    config_manager.set("test_key", "test_value")
    assert config_manager.get("test_key") == "test_value"
    # Getting a missing key should return None
    assert config_manager.get("non_existent") is None
    # Getting a missing key with a default should return default
    assert config_manager.get("non_existent", default="default") == "default"


def test_overwrite_config_key(config_manager):
    """Setting an existing key should overwrite its value."""
    config_manager.set("key", "value1")
    config_manager.set("key", "value2")
    assert config_manager.get("key") == "value2"


def test_delete_key(config_manager):
    """Deleting a specific key works."""
    config_manager.set("a", 1)
    config_manager.set("b", 2)
    config_manager.delete("a")
    assert config_manager.get("a") is None
    assert config_manager.get("b") == 2


def test_delete_all(config_manager):
    """Deleting all configuration entries clears everything."""
    config_manager.set("x", "y")
    config_manager.set("z", "w")
    config_manager.delete()
    assert config_manager.all() == {}


def test_save_and_load_config(config_manager):
    """Saving and re-loading persists the data."""
    config_manager.set("key1", "value1")
    config_manager.save()

    # Load into a new manager
    new_manager = ConfigManager(config_file=config_manager.config_file)
    new_manager.load()
    assert new_manager.get("key1") == "value1"


def test_load_invalid_json(config_manager):
    """Loading a corrupted config file should reset to empty dict."""
    with open(config_manager.config_file, "w") as f:
        f.write("invalid json")

    config_manager.load()
    assert config_manager.all() == {}


def test_file_creation_on_init(tmp_path):
    """The config file should be created if it doesn't exist."""
    file_path = tmp_path / "new_config.json"
    assert not file_path.exists()
    manager = ConfigManager(config_file=str(file_path))
    assert file_path.exists()
    assert manager.all() == {}
