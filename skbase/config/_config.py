# -*- coding: utf-8 -*-
"""Implement logic for global configuration of skbase."""
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Includes functionality like get_config, set_config, and config_context
# that is similar to scikit-learn. These elements are copyrighted by the
# scikit-learn developers, BSD-3-Clause License. For conditions see
# https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
import sys
import threading
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal  # type: ignore

from skbase.config._config_param_setting import GlobalConfigParamSetting

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = [
    "get_default_config",
    "get_config",
    "set_config",
    "reset_config",
    "config_context",
]


_CONFIG_REGISTRY: Dict[str, GlobalConfigParamSetting] = {
    "print_changed_only": GlobalConfigParamSetting(
        name="print_changed_only",
        expected_type=bool,
        allowed_values=(True, False),
        default_value=True,
    ),
    "display": GlobalConfigParamSetting(
        name="display",
        expected_type=str,
        allowed_values=("text", "diagram"),
        default_value="text",
    ),
}

_GLOBAL_CONFIG_DEFAULT: Dict[str, Any] = {
    config_settings.name: config_settings.default_value
    for config_name, config_settings in _CONFIG_REGISTRY.items()
}

global_config = _GLOBAL_CONFIG_DEFAULT.copy()

_THREAD_LOCAL_DATA = threading.local()


def _get_threadlocal_config() -> Dict[str, Any]:
    """Get a threadlocal **mutable** configuration.

    If the configuration does not exist, copy the default global configuration.

    Returns
    -------
    dict
        Threadlocal global config or copy of default global configuration.
    """
    if not hasattr(_THREAD_LOCAL_DATA, "global_config"):
        _THREAD_LOCAL_DATA.global_config = global_config.copy()
    return _THREAD_LOCAL_DATA.global_config


def get_default_config() -> Dict[str, Any]:
    """Retrieve the default global configuration.

    This will always return the default ``skbase`` global configuration.

    Returns
    -------
    config : dict
        The default configurable settings (keys) and their default values (values).

    See Also
    --------
    config_context :
        Configuration context manager.
    get_config :
        Retrieve current global configuration values.
    set_config :
        Set global configuration.
    reset_config :
        Reset configuration to ``skbase`` default.

    Examples
    --------
    >>> from skbase.config import get_default_config
    >>> get_default_config()
    {'print_changed_only': True, 'display': 'text'}
    """
    return _GLOBAL_CONFIG_DEFAULT.copy()


def get_config() -> Dict[str, Any]:
    """Retrieve current values for configuration set by :meth:`set_config`.

    Will return the default configuration if know updated configuration has
    been set by :meth:`set_config`.

    Returns
    -------
    config : dict
        The configurable settings (keys) and their default values (values).

    See Also
    --------
    config_context :
        Configuration context manager.
    get_default_config :
        Retrieve ``skbase``'s default configuration.
    set_config :
        Set global configuration.
    reset_config :
        Reset configuration to ``skbase`` default.

    Examples
    --------
    >>> from skbase.config import get_config
    >>> get_config()
    {'print_changed_only': True, 'display': 'text'}
    """
    return _get_threadlocal_config().copy()


def set_config(
    print_changed_only: Optional[bool] = None,
    display: Literal["text", "diagram"] = None,
    local_threadsafe: bool = False,
) -> None:
    """Set global configuration.

    Allows the ``skbase`` global configuration to be updated.

    Parameters
    ----------
    print_changed_only : bool, default=None
        If True, only the parameters that were set to non-default
        values will be printed when printing a BaseObject instance. For example,
        ``print(SVC())`` while True will only print 'SVC()', but would print
        'SVC(C=1.0, cache_size=200, ...)' with all the non-changed parameters
        when False. If None, the existing value won't change.
    display : {'text', 'diagram'}, default=None
        If 'diagram', instances inheritting from BaseOBject will be displayed
        as a diagram in a Jupyter lab or notebook context. If 'text', instances
        inheritting from BaseObject will be displayed as text. If None, the
        existing value won't change.
    local_threadsafe : bool, default=False
        If False, set the backend as default for all threads.

    Returns
    -------
    None
        No output returned.

    See Also
    --------
    config_context :
        Configuration context manager.
    get_default_config :
        Retrieve ``skbase``'s default configuration.
    get_config :
        Retrieve current global configuration values.
    reset_config :
        Reset configuration to default.

    Examples
    --------
    >>> from skbase.config import get_config, set_config
    >>> get_config()
    {'print_changed_only': True, 'display': 'text'}
    >>> set_config(display='diagram')
    >>> get_config()
    {'print_changed_only': True, 'display': 'diagram'}
    """
    local_config = _get_threadlocal_config()
    msg = "Attempting to set an invalid value for a global configuration.\n"
    msg += "Using current configuration value of parameter as a result.\n"
    if print_changed_only is not None:
        local_config["print_changed_only"] = _CONFIG_REGISTRY[
            "print_changed_only"
        ].get_valid_param_or_default(
            print_changed_only,
            default_value=local_config["print_changed_only"],
            msg=msg,
        )
    if display is not None:
        local_config["display"] = _CONFIG_REGISTRY[
            "display"
        ].get_valid_param_or_default(
            display, default_value=local_config["display"], msg=msg
        )

    if not local_threadsafe:
        global_config.update(local_config)

    return None


def reset_config() -> None:
    """Reset the global configuration to the default.

    Will remove any user updates to the global configuration and reset the values
    back to the ``skbase`` defaults.

    Returns
    -------
    None
        No output returned.

    See Also
    --------
    config_context :
        Configuration context manager.
    get_default_config :
        Retrieve ``skbase``'s default configuration.
    get_config :
        Retrieve current global configuration values.
    set_config :
        Set global configuration.

    Examples
    --------
    >>> from skbase.config import get_config, set_config, reset_config
    >>> get_config()
    {'print_changed_only': True, 'display': 'text'}
    >>> set_config(display='diagram')
    >>> get_config()
    {'print_changed_only': True, 'display': 'diagram'}
    >>> reset_config()
    >>> get_config()
    {'print_changed_only': True, 'display': 'text'}
    """
    default_config = get_default_config()
    set_config(**default_config)
    return None


@contextmanager
def config_context(
    print_changed_only: Optional[bool] = None,
    display: Literal["text", "diagram"] = None,
    local_threadsafe: bool = False,
) -> Iterator[None]:
    """Context manager for global configuration.

    Provides the ability to run code using different configuration without
    having to update the global config.

    Parameters
    ----------
    print_changed_only : bool, default=None
        If True, only the parameters that were set to non-default
        values will be printed when printing a BaseObject instance. For example,
        ``print(SVC())`` while True will only print 'SVC()', but would print
        'SVC(C=1.0, cache_size=200, ...)' with all the non-changed parameters
        when False. If None, the existing value won't change.
    display : {'text', 'diagram'}, default=None
        If 'diagram', instances inheritting from BaseOBject will be displayed
        as a diagram in a Jupyter lab or notebook context. If 'text', instances
        inheritting from BaseObject will be displayed as text. If None, the
        existing value won't change.
    local_threadsafe : bool, default=False
        If False, set the config as default for all threads.

    Yields
    ------
    None

    See Also
    --------
    get_default_config :
        Retrieve ``skbase``'s default configuration.
    get_config :
        Retrieve current values of the global configuration.
    set_config :
        Set global configuration.
    reset_config :
        Reset configuration to ``skbase`` default.

    Notes
    -----
    All settings, not just those presently modified, will be returned to
    their previous values when the context manager is exited.

    Examples
    --------
    >>> from skbase.config import config_context
    >>> with config_context(display='diagram'):
    ...     pass
    """
    old_config = get_config()
    set_config(
        print_changed_only=print_changed_only,
        display=display,
        local_threadsafe=local_threadsafe,
    )

    try:
        yield
    finally:
        set_config(**old_config)
