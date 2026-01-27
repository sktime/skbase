# -*- coding: utf-8 -*-
"""Global configuration management for skbase."""

from contextlib import contextmanager
from copy import deepcopy

__author__ = ["RNKuhns"]
__all__ = [
    "config_context",
    "get_config",
    "get_default_config",
    "reset_config",
    "set_config",
]

# Global configuration defaults
_DEFAULT_CONFIG = {
    "display": "diagram",
    "print_changed_only": True,
    "check_clone": False,
    "clone_config": True,
}

# Global config storage
_global_config = deepcopy(_DEFAULT_CONFIG)


def _get_global_config():
    """Get the global config dict."""
    return _global_config


def get_default_config():
    """Get the default global config.

    Returns
    -------
    dict
        Default global config.
    """
    return deepcopy(_DEFAULT_CONFIG)


def get_config():
    """Get current global config.

    Returns
    -------
    dict
        Current global config.
    """
    return deepcopy(_get_global_config())


def set_config(**config_dict):
    """Set global config values.

    Parameters
    ----------
    **config_dict : dict
        Config key-value pairs to set globally.
    """
    global_config = _get_global_config()
    global_config.update(config_dict)


def reset_config():
    """Reset global config to defaults."""
    global _global_config
    _global_config = deepcopy(_DEFAULT_CONFIG)


@contextmanager
def config_context(**config_dict):
    """Context manager for temporary config changes.

    Parameters
    ----------
    **config_dict : dict
        Config key-value pairs to set temporarily.
    """
    old_config = get_config()
    set_config(**config_dict)
    try:
        yield
    finally:
        global _global_config
        _global_config = old_config