# -*- coding: utf-8 -*-
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
"""
Registry lookup methods.

This module exports the following methods for registry lookup:

all_estimators(estimator_types, filter_tags)
    lookup and filtering of objects (BaseObject descendants)
"""

__author__ = ["fkiraly", "mloning", "katiebuc", "rnkuhns"]
# based on the sktime estimator retrieval utility of the same name
# which, in turn, is based on the sklearn estimator retrieval utility of the same name


import pkgutil
from copy import deepcopy
from importlib import import_module
from inspect import getmembers, isclass
from operator import itemgetter
from pathlib import Path

from baseobject import BaseObject


def all_estimators(
    estimator_types=None,
    filter_tags=None,
    exclude_estimators=None,
    return_names=True,
    as_dataframe=False,
    return_tags=None,
    suppress_import_stdout=True,
    package_name="baseobject",
    ignore_modules=None,
    class_lookup=None,
):
    """Get a list of all estimators in the package with name package_name.

    This function crawls the package/module and gets all classes that are objects.
    Objects means: BaseObject descendants.
    Objects retrieved can be sub-set by inheritance, tags, and exclusion conditions.

    Not included are: the base classes themselves, classes defined in test modules.

    Parameters
    ----------
    estimator_types: class, list of class, optional (default=None)
        if class_lookup is provided, can also be str or list of str
        Which kind of objects should be returned.
        if None, no filter is applied and all estimators are returned.
        if class or list of class, estimators are filtered to inherit from one of these
        if str or list of str, classes ca be aliased by strings, via class_lookup
    return_names: bool, optional (default=True)
        if True, estimator class name is included in the all_estimators()
            return in the order: name, estimator class, optional tags, either as
            a tuple or as pandas.DataFrame columns
        if False, estimator class name is removed from the all_estimators()
            return.
    filter_tags: dict of (str or list of str), optional (default=None)
        For a list of valid tag strings, use the registry.all_tags utility.
        subsets the returned estimators as follows:
            each key/value pair is statement in "and"/conjunction
                key is tag name to sub-set on
                value str or list of string are tag values
                condition is "key must be equal to value, or in set(value)"
    exclude_estimators: str, list of str, optional (default=None)
        Names of estimators to exclude.
    as_dataframe: bool, optional (default=False)
        if False, all_estimators will return a list (either a list of
            estimators or a list of tuples, see Returns)
        if True, all_estimators will return a pandas.DataFrame with named
            columns for all of the attributes being returned.
            this requires soft dependency pandas to be installed.
    return_tags: str or list of str, optional (default=None)
        Names of tags to fetch and return each estimator's value of.
        For a list of valid tag strings, use the registry.all_tags utility.
        if str or list of str,
            the tag values named in return_tags will be fetched for each
            estimator and will be appended as either columns or tuple entries.
    suppress_import_stdout : bool, optional. Default=True
        whether to suppress stdout printout upon import.
    package_name : str, optional. Default="baseobject".
        should be set to default to package or module name if used for search.
        objects will be searched inside the package/module called package_name,
        this can include sub-module dots, e.g., "package.module1.module2"
    ignore_modules : str or lits of str, optional. Default=empty list
        list of module names to ignore in search
    class_lookup : dict string -> class, optional, default=None
        dict of aliases for classes used in estimator_types

    Returns
    -------
    all_estimators will return one of the following:
        1. list of estimators, if return_names=False, and return_tags is None
        2. list of tuples (optional estimator name, class, ~optional estimator
                tags), if return_names=True or return_tags is not None.
        3. pandas.DataFrame if as_dataframe = True
        if list of estimators:
            entries are estimators matching the query,
            in alphabetical order of estimator name
        if list of tuples:
            list of (optional estimator name, estimator, optional estimator
            tags) matching the query, in alphabetical order of estimator name,
            where
            ``name`` is the estimator name as string, and is an
                optional return
            ``estimator`` is the actual estimator
            ``tags`` are the estimator's values for each tag in return_tags
                and is an optional return.
        if dataframe:
            all_estimators will return a pandas.DataFrame.
            column names represent the attributes contained in each column.
            "estimators" will be the name of the column of estimators, "names"
            will be the name of the column of estimator class names and the string(s)
            passed in return_tags will serve as column names for all columns of
            tags that were optionally requested.

    References
    ----------
    Modified version from scikit-learn's `all_estimators()`.
    """
    import io
    import sys
    import warnings

    if ignore_modules is None:
        MODULES_TO_IGNORE = []
    else:
        MODULES_TO_IGNORE = ignore_modules

    all_estimators = []
    ROOT = str(Path(__file__).parent.parent)  # sktime package root directory

    def _is_abstract(klass):
        if not (hasattr(klass, "__abstractmethods__")):
            return False
        if not len(klass.__abstractmethods__):
            return False
        return True

    def _is_private_module(module):
        return "._" in module

    def _is_ignored_module(module):
        module_parts = module.split(".")
        return any(part in MODULES_TO_IGNORE for part in module_parts)

    def _is_base_class(name):
        return name.startswith("_") or name.startswith("Base")

    def _is_estimator(name, klass):
        # Check if klass is subclass of base estimators, not an base class itself and
        # not an abstract class
        return issubclass(klass, BaseObject) and not _is_base_class(name)

    # Ignore deprecation warnings triggered at import time and from walking
    # packages
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        warnings.simplefilter("module", category=ImportWarning)
        warnings.filterwarnings(
            "ignore", category=UserWarning, message=".*has been moved to.*"
        )
        prefix = f"{package_name}."
        for _, module_name, _ in pkgutil.walk_packages(path=[ROOT], prefix=prefix):

            # Filter modules
            if _is_ignored_module(module_name) or _is_private_module(module_name):
                continue

            try:
                if suppress_import_stdout:
                    # setup text trap, import, then restore
                    sys.stdout = io.StringIO()
                    module = import_module(module_name)
                    sys.stdout = sys.__stdout__
                else:
                    module = import_module(module_name)
                classes = getmembers(module, isclass)

                # Filter classes
                estimators = [
                    (name, klass)
                    for name, klass in classes
                    if _is_estimator(name, klass)
                ]
                all_estimators.extend(estimators)
            except ModuleNotFoundError as e:
                # Skip missing soft dependencies
                if "soft dependency" not in str(e):
                    raise e
                warnings.warn(str(e), ImportWarning)

    # Drop duplicates
    all_estimators = set(all_estimators)

    # Filter based on given estimator types
    def _is_in_estimator_types(estimator, estimator_types):
        return any(isclass(x) and isinstance(estimator, x) for x in estimator_types)

    if estimator_types:
        estimator_types = _check_estimator_types(estimator_types, class_lookup)
        all_estimators = [
            (name, estimator)
            for name, estimator in all_estimators
            if _is_in_estimator_types(estimator, estimator_types)
        ]

    # Filter based on given exclude list
    if exclude_estimators:
        exclude_estimators = _check_list_of_str_or_error(
            exclude_estimators, "exclude_estimators"
        )
        all_estimators = [
            (name, estimator)
            for name, estimator in all_estimators
            if name not in exclude_estimators
        ]

    # Drop duplicates, sort for reproducibility
    # itemgetter is used to ensure the sort does not extend to the 2nd item of
    # the tuple
    all_estimators = sorted(all_estimators, key=itemgetter(0))

    if filter_tags:
        all_estimators = [
            (n, est) for (n, est) in all_estimators if _check_tag_cond(est, filter_tags)
        ]

    # remove names if return_names=False
    if not return_names:
        all_estimators = [estimator for (name, estimator) in all_estimators]
        columns = ["estimator"]
    else:
        columns = ["name", "estimator"]

    # add new tuple entries to all_estimators for each tag in return_tags:
    if return_tags:
        return_tags = _check_list_of_str_or_error(return_tags, "return_tags")
        # enrich all_estimators by adding the values for all return_tags tags:
        if all_estimators:
            if isinstance(all_estimators[0], tuple):
                all_estimators = [
                    (name, est) + _get_return_tags(est, return_tags)
                    for (name, est) in all_estimators
                ]
            else:
                all_estimators = [
                    tuple([est]) + _get_return_tags(est, return_tags)
                    for est in all_estimators
                ]
        columns = columns + return_tags

    # convert to pandas.DataFrame if as_dataframe=True
    if as_dataframe:
        all_estimators = _make_dataframe(all_estimators, columns=columns)

    return all_estimators


def _check_list_of_str_or_error(arg_to_check, arg_name):
    """Check that certain arguments are str or list of str.

    Parameters
    ----------
    arg_to_check: argument we are testing the type of
    arg_name: str,
        name of the argument we are testing, will be added to the error if
        ``arg_to_check`` is not a str or a list of str

    Returns
    -------
    arg_to_check: list of str,
        if arg_to_check was originally a str it converts it into a list of str
        so that it can be iterated over.

    Raises
    ------
    TypeError if arg_to_check is not a str or list of str
    """
    # check that return_tags has the right type:
    if isinstance(arg_to_check, str):
        arg_to_check = [arg_to_check]
    if not isinstance(arg_to_check, list) or not all(
        isinstance(value, str) for value in arg_to_check
    ):
        raise TypeError(
            f"Error in all_estimators!  Argument {arg_name} must be either\
             a str or list of str"
        )
    return arg_to_check


def _check_list_of_class_or_error(arg_to_check, arg_name):
    """Check that certain arguments are class or list of class.

    Parameters
    ----------
    arg_to_check: argument we are testing the type of
    arg_name: str,
        name of the argument we are testing, will be added to the error if
        ``arg_to_check`` is not a str or a list of str

    Returns
    -------
    arg_to_check: list of class,
        if arg_to_check was originally a class it converts it into a list of class
        so that it can be iterated over.

    Raises
    ------
    TypeError if arg_to_check is not a class or list of class
    """
    # check that return_tags has the right type:
    if isclass(arg_to_check, str):
        arg_to_check = [arg_to_check]
    if not isinstance(arg_to_check, list) or not all(
        isclass(value) for value in arg_to_check
    ):
        raise TypeError(
            f"Error in all_estimators!  Argument {arg_name} must be either\
             a class or list of class"
        )
    return arg_to_check


def _get_return_tags(estimator, return_tags):
    """Fetch a list of all tags for every_entry of all_estimators.

    Parameters
    ----------
    estimator:  BaseEstimator, an sktime estimator
    return_tags: list of str,
        names of tags to get values for the estimator

    Returns
    -------
    tags: a tuple with all the estimators values for all tags in return tags.
        a value is None if it is not a valid tag for the estimator provided.
    """
    tags = tuple(estimator.get_class_tag(tag) for tag in return_tags)
    return tags


def _check_tag_cond(estimator, filter_tags=None, as_dataframe=True):
    """Check whether estimator satisfies filter_tags condition.

    Parameters
    ----------
    estimator: BaseEstimator, an sktime estimator
    filter_tags: dict of (str or list of str), default=None
        subsets the returned estimators as follows:
            each key/value pair is statement in "and"/conjunction
                key is tag name to sub-set on
                value str or list of string are tag values
                condition is "key must be equal to value, or in set(value)"
    as_dataframe: bool, default=False
                if False, return is as described below;
                if True, return is converted into a pandas.DataFrame for pretty
                display

    Returns
    -------
    cond_sat: bool, whether estimator satisfies condition in filter_tags
    """
    if not isinstance(filter_tags, dict):
        raise TypeError("filter_tags must be a dict")

    cond_sat = True

    for (key, value) in filter_tags.items():
        if not isinstance(value, list):
            value = [value]
        cond_sat = cond_sat and estimator.get_class_tag(key) in set(value)

    return cond_sat


def _check_estimator_types(estimator_types, class_lookup=None):
    """Return list of classes corresponding to type strings.

    Parameters
    ----------
    estimator_types : str, class or list of [string or class]
    class_lookup : dict string -> class, optional, default=None

    Returns
    -------
    list of class, i-th element is:
        class_lookup[estimator_types[i]] if estimator_types[i] was a string
        estimator_types[i] otherwise
    if class_lookup is none, only checks whether estimator_types is class or list of

    Raises
    ------
    ValueError if estimator_types is not of the expected type
    """
    estimator_types = deepcopy(estimator_types)

    if not isinstance(estimator_types, list):
        estimator_types = [estimator_types]  # make iterable

    def _get_err_msg(estimator_type):
        if class_lookup is None:
            return (
                f"Parameter `estimator_type` must be None, a sclass, or a list of "
                f"class, but found: {repr(estimator_type)}"
            )
        else:
            return (
                f"Parameter `estimator_type` must be None, a string, a class, or a list"
                f" of [string or class]. Valid string values are: "
                f"{tuple(class_lookup.keys())}, but found: "
                f"{repr(estimator_type)}"
            )

    for i, estimator_type in enumerate(estimator_types):
        if not isinstance(estimator_type, (type, str)):
            raise ValueError(_get_err_msg(estimator_type))
        if isinstance(estimator_type, str):
            if estimator_type not in class_lookup.keys():
                raise ValueError(_get_err_msg(estimator_type))
            estimator_type = class_lookup[estimator_type]
            estimator_types[i] = estimator_type
        elif isinstance(estimator_type, type):
            pass
        else:
            raise ValueError(_get_err_msg(estimator_type))
    return estimator_types


def _make_dataframe(all_estimators, columns):
    """Create pandas.DataFrame for all_estimators, fct isolates pandas soft dep."""
    import pandas as pd

    return pd.DataFrame(all_estimators, columns=columns)
