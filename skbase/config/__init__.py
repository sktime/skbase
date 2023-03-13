# -*- coding: utf-8 -*-
""":mod:`skbase.config` provides tools for global configuration of ``skbase``."""
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Includes functionality like get_config, set_config, and config_context
# that is similar to scikit-learn. These elements are copyrighted by the
# scikit-learn developers, BSD-3-Clause License. For conditions see
# https://github.com/scikit-learn/scikit-learn/blob/main/COPYING

import sys
import threading
import warnings
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal  # type: ignore

__author__: List[str] = ["RNKuhns"]


@dataclass
class GlobalConfigParamSetting:
    """Define types of the setting information for a given config parameter."""

    os_environ_name: str
    expected_type: Union[type, Tuple[type]]
    allowed_values: Optional[Tuple[Any, ...]]
    default_value: Any

    def get_allowed_values(self):
        """Get `allowed_values` or empty tuple if `allowed_values` is None.

        Returns
        -------
        tuple
            Allowable values if any.
        """
        if self.allowed_values is None:
            return ()
        else:
            return self.allowed_values

    def is_valid_param_value(self, value):
        """Validate that a global configuration value is valid.

        Verifies that the value set for a global configuration parameter is valid
        based on the its configuration settings.

        Returns
        -------
        bool
            Whether a parameter value is valid.
        """
        if (
            isinstance(self.allowed_values, (list, tuple))
            or self.allowed_values is None
        ):
            allowed_values = self.allowed_values
        else:
            allowed_values = (self.allowed_values,)

        valid_param: bool
        if not isinstance(value, self.expected_type):
            valid_param = False
        elif allowed_values is not None and value not in allowed_values:
            valid_param = False
        else:
            valid_param = True
        return valid_param

    def get_valid_param_or_default(self, value):
        """Validate `value` and return default if it is not valid."""
        if self.is_valid_param_value(value):
            return value
        else:
            msg = f"{self.os_environ_name} should be one of "
            msg += f"{', '.join(map(repr, self.allowed_values))}."
            msg += "Using default value for this configuration as a result."
            warnings.warn(msg, UserWarning, stacklevel=2)
            return self.default_value


_CONFIG_REGISTRY: Dict[str, GlobalConfigParamSetting] = {
    "print_changed_only": GlobalConfigParamSetting(
        os_environ_name="SKBASE_PRINT_CHANGED_ONLY",
        expected_type=bool,
        allowed_values=(True, False),
        default_value=True,
    ),
    "display": GlobalConfigParamSetting(
        os_environ_name="SKBASE_OBJECT_DISPLAY",
        expected_type=str,
        allowed_values=("text", "diagram"),
        default_value="text",
    ),
}

_DEFAULT_GLOBAL_CONFIG: Dict[str, Any] = {
    config_name: config_info.default_value
    for config_name, config_info in _CONFIG_REGISTRY.items()
}

global_config = _DEFAULT_GLOBAL_CONFIG.copy()
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


def get_config_os_env_names() -> List[str]:
    """Retrieve the os environment names for configurable settings.

    Returns
    -------
    env_names : list
        The os environment names that can be used to set configurable settings.

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
    reset_config :
        Reset configuration to ``skbase`` default.

    Examples
    --------
    >>> from skbase.config import get_config_os_env_names
    >>> get_config_os_env_names()
    ['SKBASE_PRINT_CHANGED_ONLY', 'SKBASE_OBJECT_DISPLAY']
    """
    return [config_info.os_environ_name for config_info in _CONFIG_REGISTRY.values()]


def get_default_config() -> Dict[str, Any]:
    """Retrive the default global configuration.

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
    get_config_os_env_names :
        Retrieve os environment names that can be used to set configuration.
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
    return _DEFAULT_GLOBAL_CONFIG.copy()


def get_config() -> Dict[str, Any]:
    """Retrieve current values for configuration set by :meth:`set_config`.

    Willr return the default configuration if know updated configuration has
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
    get_config_os_env_names :
        Retrieve os environment names that can be used to set configuration.
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
    get_config_os_env_names :
        Retrieve os environment names that can be used to set configuration.
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

    if print_changed_only is not None:
        local_config["print_changed_only"] = _CONFIG_REGISTRY[
            "print_changed_only"
        ].get_valid_param_or_default(print_changed_only)
    if display is not None:
        local_config["display"] = _CONFIG_REGISTRY[
            "display"
        ].get_valid_param_or_default(display)

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
    get_config_os_env_names :
        Retrieve os environment names that can be used to set configuration.
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
    get_config_os_env_names :
        Retrieve os environment names that can be used to set configuration.
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
