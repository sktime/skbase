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


class BaseCloner:
    """Base class for clone plugins.

    Concrete classes must inherit methods:

    * check(obj) -> boolean - fast checker whether plugin applies
    * clone(obj) -> type(obj) - method to clone obj
    """

    def __init__(self, safe, clone_plugins=None):
        self.safe = safe
        self.clone_plugins = clone_plugins

    def check(self, obj):
        """Check whether the plugin applies to obj."""
        return self._check(obj)

    def clone(self, obj):
        """Return a clone of obj."""
        return self._clone(obj)

    def recursive_clone(self, obj):
        """Recursive call to _clone, for explicit code and to avoid circular imports."""
        from skbase.base._clone_base import _clone

        return _clone(obj, safe=self.safe, clone_plugins=self.clone_plugins)
        

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



class _CloneSkbase(BaseCloner):

    elif not hasattr(estimator, "get_params") or isinstance(estimator, type):


class _CloneSklearn(BaseCloner):
    """Clone plugin for scikit-learn BaseEstimator descendants."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""


class _CloneGetParams(BaseCloner):
    """Clone plugin for objects that implement get_params but are not the above."""

    def _check(self, obj):
        """Check whether the plugin applies to obj."""
        return hasattr(obj, "get_params")


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
    _CloneSklearn,
    _CloneSkbase,
    _CloneCatchAll,
]
