# -*- coding: utf-8 -*-
"""Tests for global config functionality."""

from skbase.config import (
    config_context,
    get_config,
    get_default_config,
    reset_config,
    set_config,
)


def test_get_default_config():
    """Test get_default_config returns correct defaults."""
    defaults = get_default_config()
    expected = {
        "display": "diagram",
        "print_changed_only": True,
        "check_clone": False,
        "clone_config": True,
    }
    assert defaults == expected


def test_get_config():
    """Test get_config returns current global config."""
    reset_config()
    config = get_config()
    assert config == get_default_config()


def test_set_config():
    """Test set_config updates global config."""
    reset_config()
    set_config(display="text", check_clone=True)
    config = get_config()
    assert config["display"] == "text"
    assert config["check_clone"] is True
    assert config["print_changed_only"] is True  # unchanged


def test_reset_config():
    """Test reset_config resets to defaults."""
    set_config(display="text")
    reset_config()
    config = get_config()
    assert config == get_default_config()


def test_config_context():
    """Test config_context temporarily changes config."""
    reset_config()
    original_config = get_config()

    with config_context(display="text", check_clone=True):
        inner_config = get_config()
        assert inner_config["display"] == "text"
        assert inner_config["check_clone"] is True

    # Should be back to original
    final_config = get_config()
    assert final_config == original_config


def test_config_context_nested():
    """Test nested config_context."""
    reset_config()

    with config_context(display="text"):
        assert get_config()["display"] == "text"

        with config_context(print_changed_only=False):
            assert get_config()["display"] == "text"
            assert get_config()["print_changed_only"] is False

        assert get_config()["display"] == "text"
        assert get_config()["print_changed_only"] is True  # back to default
