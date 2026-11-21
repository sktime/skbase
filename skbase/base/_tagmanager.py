# -*- coding: utf-8 -*-
"""Mixin class for flag and configuration settings management."""

# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)

__author__ = ["fkiraly"]
__all__ = ["_FlagManager"]


import inspect
from copy import deepcopy
from functools import lru_cache

# builtin container types whose values are copied before flags are returned,
# matched by exact type so that subclasses (e.g., namedtuple) keep their type
_CONTAINER_TYPES = (list, dict, set, tuple)


class _FlagManager:
    """Mixin class for flag and configuration settings management."""

    @staticmethod
    def _copy_containers(value):
        """Copy builtin containers in ``value`` recursively, share other objects.

        Parameters
        ----------
        value : any
            Flag value to copy.

        Returns
        -------
        value_copy : any
            ``value`` with every nested ``list``, ``dict``, ``set`` and ``tuple``
            rebuilt, so that in-place changes to the copy do not affect ``value``.
            Objects of any other type are returned unchanged.
        """
        copy_fn = _FlagManager._copy_containers
        value_type = type(value)
        if value_type is dict:
            return {key: copy_fn(item) for key, item in value.items()}
        if value_type is list:
            return [copy_fn(item) for item in value]
        if value_type is tuple:
            return tuple(copy_fn(item) for item in value)
        if value_type is set:
            return set(value)
        return value

    @classmethod
    def _copied_class_flags(cls, flag_attr_name="_flags"):
        """Get the cached class flags as a dict that is safe to mutate.

        Parameters
        ----------
        flag_attr_name : str, default = "_flags"
            Name of the flag attribute that is read.

        Returns
        -------
        collected_flags : dict
            Fresh dict of class flags. Flat builtin containers are shallow-copied,
            nested ones are copied with ``_copy_containers``, all other values
            are shared with the cache.
        """
        flags, flat_keys, nested_keys = _collect_class_flags_cached(cls, flag_attr_name)
        collected_flags = dict(flags)
        for key in flat_keys:
            collected_flags[key] = flags[key].copy()
        for key in nested_keys:
            collected_flags[key] = cls._copy_containers(flags[key])
        return collected_flags

    @classmethod
    def _get_class_flags(cls, flag_attr_name="_flags"):
        """Get class flags from estimator class and all its parent classes.

        Parameters
        ----------
        flag_attr_name : str, default = "_flags"
            Name of the flag attribute that is read.

        Returns
        -------
        collected_flags : dict
            Dictionary of flag name : flag value pairs. Collected from _flags
            class attribute via nested inheritance. NOT overridden by dynamic
            flags set by set_flags or clone_flags.
        """
        return cls._copied_class_flags(flag_attr_name)

    @classmethod
    def _get_class_flag(
        cls, flag_name, flag_value_default=None, flag_attr_name="_flags"
    ):
        """Get flag value from estimator class (only class flags).

        Parameters
        ----------
        flag_name : str
            Name of flag value.
        flag_value_default : any type
            Default/fallback value if flag is not found.
        flag_attr_name : str, default = "_flags"
            Name of the flag attribute that is read.

        Returns
        -------
        flag_value
            Value of `flag_name` flag in self. If not found, `flag_value_default`.
        """
        collected_flags = cls._get_class_flags(flag_attr_name=flag_attr_name)

        return collected_flags.get(flag_name, flag_value_default)

    def _init_flags(self, flag_attr_name="_flags"):
        """Create dynamic flag dictionary in self.

        Should be called in __init__ of the host class.
        Creates attribute [flag_attr_name]_dynamic containing an empty dict.

        Parameters
        ----------
        flag_attr_name : str, default = "_flags"
            Name of the flag attribute that is read.

        Returns
        -------
        self : reference to self
        """
        setattr(self, f"{flag_attr_name}_dynamic", {})
        return self

    def _get_flags(self, flag_attr_name="_flags"):
        """Get flags from estimator class and dynamic flag overrides.

        Parameters
        ----------
        flag_attr_name : str, default = "_flags"
            Name of the flag attribute that is read.

        Returns
        -------
        collected_flags : dict
            Dictionary of flag name : flag value pairs. Collected from flag_attr_name
            class attribute via nested inheritance and then any overrides
            and new flags from [flag_attr_name]_dynamic object attribute.
        """
        collected_flags = self._copied_class_flags(flag_attr_name)

        if hasattr(self, f"{flag_attr_name}_dynamic"):
            dynamic_flags = getattr(self, f"{flag_attr_name}_dynamic")
            for key, value in dynamic_flags.items():
                collected_flags[key] = self._copy_containers(value)

        return collected_flags

    def _get_flag(
        self,
        flag_name,
        flag_value_default=None,
        raise_error=True,
        flag_attr_name="_flags",
    ):
        """Get flag value from estimator class and dynamic flag overrides.

        Parameters
        ----------
        flag_name : str
            Name of flag to be retrieved.
        flag_value_default : any type, default=None
            Default/fallback value if flag is not found
        raise_error : bool
            Whether a `ValueError` is raised when the flag is not found.
        flag_attr_name : str, default = "_flags"
            Name of the flag attribute that is read.

        Returns
        -------
        flag_value :
            Value of the `flag_name` flag in self. If not found, returns an error if
            raise_error is True, otherwise it returns `flag_value_default`.

        Raises
        ------
        ValueError
            if `raise_error` is `True`, i.e.,
            if `flag_name` is not in `self.get_flags().keys()`
        """
        collected_flags = self._get_flags(flag_attr_name=flag_attr_name)

        flag_value = collected_flags.get(flag_name, flag_value_default)

        if raise_error and flag_name not in collected_flags.keys():
            raise ValueError(f"Tag with name {flag_name} could not be found.")

        return flag_value

    def _set_flags(self, flag_attr_name="_flags", **flag_dict):
        """Set dynamic flags to given values.

        Parameters
        ----------
        flag_dict : dict
            Dictionary of flag name : flag value pairs.
        flag_attr_name : str, default = "_flags"
            Name of the flag attribute that is read.

        Returns
        -------
        self
            Reference to self.

        Notes
        -----
        Changes object state by setting flag values in flag_dict as dynamic flags
        in self.
        """
        flag_update = deepcopy(flag_dict)
        dynamic_flags = f"{flag_attr_name}_dynamic"
        if hasattr(self, dynamic_flags):
            getattr(self, dynamic_flags).update(flag_update)
        else:
            setattr(self, dynamic_flags, flag_update)

        return self

    def _clone_flags(self, estimator, flag_names=None, flag_attr_name="_flags"):
        """clone/mirror flags from another estimator as dynamic override.

        Parameters
        ----------
        estimator : estimator inheriting from :class:BaseEstimator
        flag_names : str or list of str, default = None
            Names of flags to clone. If None then all flags in estimator are used
            as `flag_names`.
        flag_attr_name : str, default = "_flags"
            Name of the flag attribute that is read.

        Returns
        -------
        self
            Reference to self.

        Notes
        -----
        Changes object state by setting flag values in flag_set from estimator as
        dynamic flags in self.
        """
        flags_est = deepcopy(estimator._get_flags(flag_attr_name=flag_attr_name))

        # if flag_set is not passed, default is all flags in estimator
        if flag_names is None:
            flag_names = flags_est.keys()
        else:
            # if flag_set is passed, intersect keys with flags in estimator
            if not isinstance(flag_names, list):
                flag_names = [flag_names]
            flag_names = [key for key in flag_names if key in flags_est.keys()]

        update_dict = {key: flags_est[key] for key in flag_names}

        self._set_flags(flag_attr_name=flag_attr_name, **update_dict)

        return self


@lru_cache(maxsize=None)
def _collect_class_flags_cached(cls, flag_attr_name):
    """Walk the MRO once per (cls, flag_attr_name) and cache the result.

    Returns
    -------
    collected_flags : dict
        Class flags collected along the MRO. This is the shared cached object,
        callers must not mutate it or hand it out, see
        ``_FlagManager._copied_class_flags``.
    flat_keys : tuple of str
        Keys whose value is a ``list``, ``dict`` or ``set`` that contains no
        builtin container, a shallow copy of these is enough.
    nested_keys : tuple of str
        Keys whose value is a ``list``, ``dict``, ``set`` or ``tuple`` that
        contains a builtin container, these need ``_copy_containers``.
    """
    collected_flags = {}
    for parent_class in reversed(inspect.getmro(cls)):
        if parent_class is object:
            continue
        if flag_attr_name in parent_class.__dict__:
            more_flags = parent_class.__dict__[flag_attr_name]
            collected_flags.update(more_flags)

    flat_keys = []
    nested_keys = []
    for key, value in collected_flags.items():
        value_type = type(value)
        if value_type not in _CONTAINER_TYPES:
            continue
        items = value.values() if value_type is dict else value
        if any(type(item) in _CONTAINER_TYPES for item in items):
            nested_keys.append(key)
        elif value_type is not tuple:
            flat_keys.append(key)

    return collected_flags, tuple(flat_keys), tuple(nested_keys)
