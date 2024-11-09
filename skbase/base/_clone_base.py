# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Elements of BaseObject reuse code developed in scikit-learn. These elements
# are copyrighted by the scikit-learn developers, BSD-3-Clause License. For
# conditions see https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
"""Logic and plugins for cloning objects.

This module contains logic for cloning objects:

_clone(estimator, *, safe=True, plugins=None) - central entry point for cloning
_check_clone(original, clone) - validation utility to check clones

Default plugins for _clone are stored in _clone_plugins:

DEFAULT_CLONE_PLUGINS - list with default plugins for cloning

Each element of DEFAULT_CLONE_PLUGINS inherits from BaseCloner, with methods:

* check(obj) -> boolean - fast checker whether plugin applies
* clone(obj) -> type(obj) - method to clone obj
"""
from copy import deepcopy

from skbase.base._clone_plugins import DEFAULT_CLONE_PLUGINS


# Adapted from sklearn's `_clone_parametrized()`
def _clone(estimator, *, safe=True, clone_plugins=None):
    """Construct a new unfitted estimator with the same parameters.

    Clone does a deep copy of the model in an estimator
    without actually copying attached data. It returns a new estimator
    with the same parameters that has not been fitted on any data.

    Parameters
    ----------
    estimator : {list, tuple, set} of estimator instance or a single estimator instance
        The estimator or group of estimators to be cloned.
    safe : bool, default=True
        If ``safe`` is False, clone will fall back to a deep copy on objects
        that are not estimators.
    clone_plugins : list of BaseCloner clone plugins, concrete descendant classes.
        Must implement ``_check`` and ``_clone`` method, see ``BaseCloner`` interface.
        If passed, will work through clone plugins in ``clone_plugins``
        before working through ``DEFAULT_CLONE_PLUGINS``. To override
        a cloner in ``DEAULT_CLONE_PLUGINS``, simply ensure a cloner with
        the same ``_check`` logis is present in ``clone_plugins``.

    Returns
    -------
    estimator : object
        The deep copy of the input, an estimator if input is an estimator.

    Notes
    -----
    If the estimator's `random_state` parameter is an integer (or if the
    estimator doesn't have a `random_state` parameter), an *exact clone* is
    returned: the clone and the original estimator will give the exact same
    results. Otherwise, *statistical clone* is returned: the clone might
    return different results from the original estimator. More details can be
    found in :ref:`randomness`.
    """
    # handle cloning plugins:
    # if no plugins provided by user, work through the DEFAULT_CLONE_PLUGINS
    # if provided by user, work through user provided plugins first, then defaults
    if clone_plugins is not None:
        clone_plugins = clone_plugins.copy()
        clone_plugins.append(DEFAULT_CLONE_PLUGINS.copy())
    else:
        clone_plugins = DEFAULT_CLONE_PLUGINS

    for cloner_plugin in clone_plugins:
        cloner = cloner_plugin(safe=safe, clone_plugins=clone_plugins)
        if cloner.check(obj=estimator):
            return cloner.clone(obj=estimator)


    estimator_type = type(estimator)

    klass = estimator.__class__
    new_object_params = estimator.get_params(deep=False)
    for name, param in new_object_params.items():
        new_object_params[name] = _clone(param, safe=False)
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

    # This is an extension to the original sklearn implementation
    if isinstance(estimator, BaseObject) and estimator.get_config()["clone_config"]:
        new_object.set_config(**estimator.get_config())

    if clone_attrs is not None:
        for attr in clone_attrs:
            if hasattr(estimator, attr):
                setattr(new_object, attr, getattr(estimator, attr))

    return new_object


def _check_clone(original, clone):
    from skbase.utils.deep_equals import deep_equals

    self_params = original.get_params(deep=False)

    # check that all attributes are written to the clone
    for attrname in self_params.keys():
        if not hasattr(clone, attrname):
            raise RuntimeError(
                f"error in {original}.clone, __init__ must write all arguments "
                f"to self and not mutate them, but {attrname} was not found. "
                f"Please check __init__ of {original}."
            )

    clone_attrs = {attr: getattr(clone, attr) for attr in self_params.keys()}

    # check equality of parameters post-clone and pre-clone
    clone_attrs_valid, msg = deep_equals(self_params, clone_attrs, return_msg=True)
    if not clone_attrs_valid:
        raise RuntimeError(
            f"error in {original}.clone, __init__ must write all arguments "
            f"to self and not mutate them, but this is not the case. "
            f"Error on equality check of arguments (x) vs parameters (y): {msg}"
        )

