# -*- coding: utf-8 -*-
"""Test configuration functionality."""
import pytest

from skbase.config import (
    GlobalConfigParamSetting,
    config_context,
    get_config,
    get_default_config,
    reset_config,
    set_config,
)
from skbase.config._config import _CONFIG_REGISTRY, _DEFAULT_GLOBAL_CONFIG

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


@pytest.mark.parametrize("allowed_values", (None, (), "something", range(1, 8)))
def test_global_config_param_get_allowed_values(allowed_values):
    """Test GlobalConfigParamSetting behavior works as expected."""
    some_config_param = GlobalConfigParamSetting(
        name="some_param",
        os_environ_name="SKBASE_OBJECT_DISPLAY",
        expected_type=str,
        allowed_values=allowed_values,
        default_value="text",
    )
    # Verify we always coerce output of get_allowed_values to tuple
    values = some_config_param.get_allowed_values()
    assert isinstance(values, list)


@pytest.mark.parametrize("value", (None, (), "wrong_string", "text", range(1, 8)))
def test_global_config_param_is_valid_param_value(value):
    """Test GlobalConfigParamSetting behavior works as expected."""
    some_config_param = GlobalConfigParamSetting(
        name="some_param",
        os_environ_name="SKBASE_OBJECT_DISPLAY",
        expected_type=str,
        allowed_values=("text", "diagram"),
        default_value="text",
    )
    # Verify we correctly identify invalid parameters
    if value in ("text", "diagram"):
        expected_valid = True
    else:
        expected_valid = False
    assert some_config_param.is_valid_param_value(value) == expected_valid


def test_get_default_config(global_config_default):
    """Test get_default_config alwasy returns the default config."""
    assert get_default_config() == global_config_default
    set_config(print_changed_only=False)
    assert get_default_config() == global_config_default


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
def test_reset_config_resets_the_config(
    print_changed_only, display, global_config_default
):
    """Verify that get_config returns default config if reset_config run."""
    set_config(print_changed_only=print_changed_only, display=display)
    reset_config()
    retrieved_config = get_config()

    msg = "`get_config` does not return expected values after `reset_config`.\n"
    msg += "`After reset_config is run, get_config` should return defaults.\n"
    msg += f"Expected {global_config_default}, but returned {retrieved_config}."
    assert retrieved_config == global_config_default, msg
    reset_config()


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
    reset_config()


def test_set_config_behavior_invalid_value():
    """Test set_config uses default and raises warning when setting invalid value."""
    reset_config()
    original_config = get_config().copy()
    with pytest.warns(UserWarning, match=r"Attempting to set an invalid value.*"):
        set_config(print_changed_only="False")

    assert get_config() == original_config

    original_config = get_config().copy()
    with pytest.warns(UserWarning, match=r"Attempting to set an invalid value.*"):
        set_config(print_changed_only=7)

    assert get_config() == original_config
    reset_config()
