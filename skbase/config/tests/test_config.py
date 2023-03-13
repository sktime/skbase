# -*- coding: utf-8 -*-
"""Test configuration functionality."""
import pytest

from skbase.config import (
    _CONFIG_REGISTRY,
    _DEFAULT_GLOBAL_CONFIG,
    config_context,
    get_config,
    get_config_os_env_names,
    get_default_config,
    reset_config,
    set_config,
)

PRINT_CHANGE_ONLY_VALUES = _CONFIG_REGISTRY["print_changed_only"].get_allowed_values()
DISPLAY_VALUES = _CONFIG_REGISTRY["display"].get_allowed_values()


@pytest.fixture
def config_registry():
    """Config registry fixture."""
    return _CONFIG_REGISTRY


@pytest.fixture
def global_config_default():
    """Config registry fixture."""
    return _DEFAULT_GLOBAL_CONFIG


def test_get_config_os_env_names(config_registry):
    """Verify that get_config_os_env_names returns expected values."""
    os_env_names = get_config_os_env_names()
    expected_os_env_names = [
        config_info.os_environ_name for config_info in config_registry.values()
    ]
    msg = "`get_config_os_env_names` does not return expected value.\n"
    msg += f"Expected {expected_os_env_names}, but returned {os_env_names}."
    assert os_env_names == expected_os_env_names, msg


def test_get_default_config(global_config_default):
    """Verify that get_default_config returns default global config values."""
    retrieved_default = get_default_config()
    msg = "`get_default_config` does not return expected values.\n"
    msg += f"Expected {global_config_default}, but returned {retrieved_default}."
    assert retrieved_default == global_config_default, msg


@pytest.mark.parametrize("print_changed_only", PRINT_CHANGE_ONLY_VALUES)
@pytest.mark.parametrize("display", DISPLAY_VALUES)
def test_set_config_then_get_config_returns_expected_value(print_changed_only, display):
    """Verify that get_config returns set config values if set_config run."""
    set_config(print_changed_only=print_changed_only, display=display)
    retrieved_default = get_config()
    expected_config = {"print_changed_only": print_changed_only, "display": display}
    msg = "`get_config` used after `set_config` does not return expected values.\n"
    msg += "After set_config is run, get_config should return the set values.\n "
    msg += f"Expected {expected_config}, but returned {retrieved_default}."
    assert retrieved_default == expected_config, msg


@pytest.mark.parametrize("print_changed_only", PRINT_CHANGE_ONLY_VALUES)
@pytest.mark.parametrize("display", DISPLAY_VALUES)
def test_reset_config_resets_the_config(print_changed_only, display):
    """Verify that get_config returns default config if reset_config run."""
    default_config = get_default_config()
    set_config(print_changed_only=print_changed_only, display=display)
    reset_config()
    retrieved_config = get_config()

    msg = "`get_config` does not return expected values after `reset_config`.\n"
    msg += "`After reset_config is run, get_config` should return defaults.\n"
    msg += f"Expected {default_config}, but returned {retrieved_config}."
    assert retrieved_config == default_config, msg


@pytest.mark.parametrize("print_changed_only", PRINT_CHANGE_ONLY_VALUES)
@pytest.mark.parametrize("display", DISPLAY_VALUES)
def test_config_context(print_changed_only, display):
    """Verify that config_context affects context but not overall configuration."""
    # Make sure config is reset to default values then retrieve it
    reset_config()
    retrieved_config = get_config()
    # Now lets make sure the config_context is changing the context of those values
    # within the scope of the context manager as expected
    for print_changed_only in (True, False):
        with config_context(print_changed_only=print_changed_only, display=display):
            retrieved_context_config = get_config()
        expected_config = {"print_changed_only": print_changed_only, "display": display}
        msg = "`get_config` does not return expected values within `config_context`.\n"
        msg += "`get_config` should return config defined by `config_context`.\n"
        msg += f"Expected {expected_config}, but returned {retrieved_context_config}."
        assert retrieved_context_config == expected_config, msg

    # Outside of the config_context we should have not affected the retrieved config
    # set by call to reset_config()
    config_post_config_context = get_config()
    msg = "`get_config` does not return expected values after `config_context`a.\n"
    msg += "`config_context` should not affect configuration outside its context.\n"
    msg += f"Expected {config_post_config_context}, but returned {retrieved_config}."
    assert retrieved_config == config_post_config_context, msg
