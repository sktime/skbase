# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Elements of BaseObject reuse code developed in scikit-learn. These elements
# are copyrighted by the scikit-learn developers, BSD-3-Clause License. For
# conditions see https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
"""Logic and plugins for cloning objects - default plugins.

This module contains default plugins for _clone, from _clone_base.

DEFAULT_CLONE_PLUGINS - list with default plugins for cloning

Each element of DEFAULT_CLONE_PLUGINS inherits from BaseCloner, with methods:

* check(obj) -> boolean - fast checker whether plugin applies
* clone(obj) -> type(obj) - method to clone obj
"""
from inspect import isclass

from skbase.utils.dependencies import _check_soft_dependencies

SKLEARN_PRESENT = _check_soft_dependencies("scikit-learn")

# _sklearn_clone is imported at module level for speed
# we wrap this in try/except to avoid exceptions on skbase init
if SKLEARN_PRESENT:
    try:
        from sklearn import clone as _sklearn_clone
    except Exception:
        pass


class BaseCloner:
    """Base class for clone plugins.

    Concrete classes must inherit methods:

    * check(obj) -> boolean - fast checker whether plugin applies
    * clone(obj) -> type(obj) - method to clone obj
    """

    def __init__(self, safe, clone_plugins=None, base_cls=None):
        self.safe = safe
        self.clone_plugins = clone_plugins
        self.base_cls = base_cls

    def check(self, obj):
        """Check whether the plugin applies to obj."""
        try:
            return self._check(obj)
        except Exception:
            return False

    def clone(self, obj):
        """Return a clone of obj."""
        return self._clone(obj)

    def recursive_clone(self, obj):
        """Recursive call to _clone, for explicit code and to avoid circular imports."""
        from skbase.base._clone_base import _clone

        recursion_kwargs = {
            "safe": self.safe,
            "clone_plugins": self.clone_plugins,
            "base_cls": self.base_cls,
        }
        return _clone(obj, **recursion_kwargs)


class _CloneClass(BaseCloner):
    """Clone plugin for classes. Returns the class."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""
        return isclass(obj)

    def _clone(self, obj):
        """Return a clone of obj."""
        return obj


class _CloneDict(BaseCloner):
    """Clone plugin for dicts. Performs recursive cloning."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""
        return isinstance(obj, dict)

    def _clone(self, obj):
        """Return a clone of obj."""
        _clone = self.recursive_clone
        return {k: _clone(v) for k, v in obj.items()}


class _CloneListTupleSet(BaseCloner):
    """Clone plugin for lists, tuples, sets. Performs recursive cloning."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""
        return isinstance(obj, (list, tuple, set, frozenset))

    def _clone(self, obj):
        """Return a clone of obj."""
        _clone = self.recursive_clone
        return type(obj)([_clone(e) for e in obj])


def _default_clone(estimator, recursive_clone):
    """Default clone routinge used in skbase native and generic get_params clone."""
    klass = estimator.__class__
    new_object_params = estimator.get_params(deep=False)
    for name, param in new_object_params.items():
        new_object_params[name] = recursive_clone(param)
    new_object = klass(**new_object_params)
    params_set = new_object.get_params(deep=False)

    # quick sanity check of the parameters of the clone
    for name in new_object_params:
        param1 = new_object_params[name]
        param2 = params_set[name]
        if param1 is not param2:
            raise RuntimeError(
                "Cannot clone object %s, as the constructor "
                "either does not set or modifies parameter %s" % (estimator, name)
            )

    return new_object


class _CloneSkbase(BaseCloner):
    """Clone plugin for scikit-base BaseObject descendants."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""
        return isinstance(obj, self.base_cls)

    def _clone(self, obj):
        """Return a clone of obj."""
        new_object = _default_clone(estimator=obj)

        # Ensure that configs are retained in the new object
        if obj.get_config()["clone_config"]:
            new_object.set_config(**obj.get_config())

        return new_object


class _CloneSklearn(BaseCloner):
    """Clone plugin for scikit-learn BaseEstimator descendants."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""
        if not SKLEARN_PRESENT:
            return False

        from sklearn.base import BaseEstimator

        return isinstance(obj, BaseEstimator)

    def _clone(self, obj):
        """Return a clone of obj."""
        return _sklearn_clone(obj)


class _CloneGetParams(BaseCloner):
    """Clone plugin for objects that implement get_params but are not the above."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""
        return hasattr(obj, "get_params")

    def _clone(self, obj):
        """Return a clone of obj."""
        return _default_clone(estimator=obj)


class _CloneCatchAll(BaseCloner):
    """Catch-all plug-in to deal, catches all objects at the end of list."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""
        return True

    def _clone(self, obj):
        """Return a clone of obj."""
        from copy import deepcopy

        if not self.safe:
            return deepcopy(obj)
        else:
            raise TypeError(
                "Cannot clone object '%s' (type %s): "
                "it does not seem to be a scikit-base object or scikit-learn "
                "estimator, as it does not implement a "
                "'get_params' method." % (repr(obj), type(obj))
            )


DEFAULT_CLONE_PLUGINS = [
    _CloneClass,
    _CloneDict,
    _CloneListTupleSet,
    _CloneSkbase,
    _CloneSklearn,
    _CloneGetParams,
    _CloneCatchAll,
]