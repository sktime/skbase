# -*- coding: utf-8 -*-
"""Testing utility to compare equality in value for nested objects.

Objects compared can have one of the following valid types:
    types compatible with != comparison
    pd.Series, pd.DataFrame, np.ndarray
    lists, tuples, or dicts of a valid type (recursive)
"""
from inspect import isclass, signature
from typing import List

from skbase.utils.deep_equals._common import _make_ret

__author__: List[str] = ["fkiraly"]
__all__: List[str] = ["deep_equals"]


# flag variables for available soft dependencies
# we are not using _check_soft_dependencies in order to keep
# this utility uncoupled from the dependency on "packaging", of _check_soft_dependencies
def _softdep_available(importname):
    from importlib import import_module

    try:
        import_module(importname)
    except ModuleNotFoundError:
        return False
    else:
        return True


def deep_equals(x, y, return_msg=False, plugins=None):
    """Test two objects for equality in value.

    Correct if x/y are one of the following valid types:
        types compatible with != comparison
        pd.Series, pd.DataFrame, np.ndarray
        lists, tuples, or dicts of a valid type (recursive)

    Important note:
        this function will return "not equal" if types of x,y are different
        for instant, bool and numpy.bool are *not* considered equal

    Parameters
    ----------
    x : object
    y : object
    return_msg : bool, optional, default=False
        whether to return informative message about what is not equal
    plugins : list, optional, default=None
        optional additional deep_equals plugins to use
        will be appended to the default plugins from ``deep_equals_custom``
        see ``deep_equals_custom`` for details of signature of plugins

    Returns
    -------
    is_equal: bool - True if x and y are equal in value
        x and y do not need to be equal in reference
    msg : str, only returned if return_msg = True
        indication of what is the reason for not being equal
            concatenation of the following strings:
            .type - type is not equal
            .class - both objects are classes but not equal
            .len - length is not equal
            .value - value is not equal
            .keys - if dict, keys of dict are not equal
                    if class/object, names of attributes and methods are not equal
            .dtype - dtype of pandas or numpy object is not equal
            .index - index of pandas object is not equal
            .series_equals, .df_equals, .index_equals - .equals of pd returns False
            [i] - if tuple/list: i-th element not equal
            [key] - if dict: value at key is not equal
            [colname] - if pandas.DataFrame: column with name colname is not equal
            != - call to generic != returns False
    """
    # call deep_equals_custom with default plugins
    plugins_default = [
        _numpy_equals_plugin,
        _pandas_equals_plugin,
        _fh_equals_plugin,
    ]

    if plugins is not None:
        plugins_inner = plugins_default + plugins
    else:
        plugins_inner = plugins_default

    res = deep_equals_custom(x, y, return_msg=return_msg, plugins=plugins_inner)
    return res


def _is_pandas(x):
    import pandas as pd

    return isinstance(x, (pd.Series, pd.DataFrame, pd.Index))


def _is_npndarray(x):
    clstr = type(x).__name__
    return clstr == "ndarray"


def _is_npnan(x):
    numpy_available = _softdep_available("numpy")

    if numpy_available:
        import numpy as np

        return isinstance(x, float) and np.isnan(x)

    else:
        return False


def _coerce_list(x):
    """Coerce x to list."""
    if not isinstance(x, (list, tuple)):
        x = [x]
    if isinstance(x, tuple):
        x = list(x)

    return x


def _numpy_equals_plugin(x, y, return_msg=False):
    numpy_available = _softdep_available("numpy")

    if not numpy_available or not _is_npndarray(x):
        return None
    else:
        import numpy as np

    ret = _make_ret(return_msg)

    if x.dtype != y.dtype:
        return ret(False, f".dtype, x.dtype = {x.dtype} != y.dtype = {y.dtype}")
    return ret(np.array_equal(x, y, equal_nan=True), ".values")


def _pandas_equals_plugin(x, y, return_msg=False, deep_equals=None):
    pandas_available = _softdep_available("pandas")

    if not pandas_available or not _is_pandas(x):
        return None

    # pandas is a soft dependency, so we compare pandas objects separately
    #   and only if pandas is installed in the environment
    res = _pandas_equals(x, y, return_msg=return_msg, deep_equals=deep_equals)
    return res


def _pandas_equals(x, y, return_msg=False, deep_equals=None):
    import pandas as pd

    ret = _make_ret(return_msg)

    if isinstance(x, pd.Series):
        if x.dtype != y.dtype:
            return ret(False, ".dtype, x.dtype= {} != y.dtype = {}", [x.dtype, y.dtype])
        # if columns are object, recurse over entries and index
        if x.dtype == "object":
            index_equal = x.index.equals(y.index)
            values_equal, values_msg = deep_equals(
                list(x.to_numpy()), list(y.to_numpy()), return_msg=True
            )
            if not values_equal:
                msg = ".values" + values_msg
            elif not index_equal:
                msg = f".index, x.index: {x.index}, y.index: {y.index}"
            else:
                msg = ""
            return ret(index_equal and values_equal, msg)
        else:
            return ret(x.equals(y), ".series_equals, x = {} != y = {}", [x, y])
    elif isinstance(x, pd.DataFrame):
        # check column names for equality
        if not x.columns.equals(y.columns):
            return ret(
                False,
                ".columns, x.columns = {} != y.columns = {}",
                [x.columns, y.columns],
            )
        # check dtypes for equality
        if not x.dtypes.equals(y.dtypes):
            return ret(
                False, f".dtypes, x.dtypes = {x.dtypes} != y.dtypes = {y.dtypes}"
            )
        # if columns, dtypes are equal and at least one is object, recurse over Series
        # if columns are equal and at least one is object, recurse over Series
        if sum(x.dtypes == "object") > 0:
            for c in x.columns:
                is_equal, msg = deep_equals(x[c], y[c], return_msg=True)
                if not is_equal:
                    return ret(False, f"[{c!r}]" + msg)
            return ret(True, "")
        else:
            return ret(x.equals(y), ".df_equals, x = {} != y = {}", [x, y])
    elif isinstance(x, pd.Index):
        return ret(x.equals(y), ".index_equals, x = {} != y = {}", [x, y])
    else:
        raise RuntimeError(
            f"Unexpected type of pandas object in _pandas_equals: type(x)={type(x)},"
            f" type(y)={type(y)}, both should be one of "
            "pd.Series, pd.DataFrame, pd.Index"
        )


def _tuple_equals(x, y, return_msg=False):
    """Test two tuples or lists for equality.

    Correct if tuples/lists contain the following valid types:
        types compatible with != comparison
        pd.Series, pd.DataFrame, np.ndarray
        lists, tuples, or dicts of a valid type (recursive)

    Parameters
    ----------
    x: tuple or list
    y: tuple or list
    return_msg : bool, optional, default=False
        whether to return informative message about what is not equal

    Returns
    -------
    is_equal: bool - True if x and y are equal in value
        x and y do not need to be equal in reference
    msg : str, only returned if return_msg = True
        indication of what is the reason for not being equal
            concatenation of the following elements:
            .len - length is not equal
            [i] - i-th element not equal
    """
    ret = _make_ret(return_msg)

    n = len(x)

    if n != len(y):
        return ret(False, f".len, x.len = {n} != y.len = {len(y)}")

    # we now know dicts are same length
    for i in range(n):
        xi = x[i]
        yi = y[i]

        # recurse through xi/yi
        is_equal, msg = deep_equals(xi, yi, return_msg=True)
        if not is_equal:
            return ret(False, f"[{i}]" + msg)

    return ret(True, "")


def _dict_equals(x, y, return_msg=False):
    """Test two dicts for equality.

    Correct if dicts contain the following valid types:
        types compatible with != comparison
        pd.Series, pd.DataFrame, np.ndarray
        lists, tuples, or dicts of a valid type (recursive)

    Parameters
    ----------
    x: dict
    y: dict
    return_msg : bool, optional, default=False
        whether to return informative message about what is not equal

    Returns
    -------
    is_equal: bool - True if x and y are equal in value
        x and y do not need to be equal in reference
    msg : str, only returned if return_msg = True
        indication of what is the reason for not being equal
            concatenation of the following strings:
            .keys - keys are not equal
            [key] - values at key is not equal
    """
    ret = _make_ret(return_msg)

    xkeys = set(x.keys())
    ykeys = set(y.keys())

    if xkeys != ykeys:
        xmy = xkeys.difference(ykeys)
        ymx = ykeys.difference(xkeys)
        diffmsg = ".keys,"
        if len(xmy) > 0:
            diffmsg += f" x.keys-y.keys = {xmy}."
        if len(ymx) > 0:
            diffmsg += f" y.keys-x.keys = {ymx}."
        return ret(False, diffmsg)

    # we now know that xkeys == ykeys
    for key in xkeys:
        xi = x[key]
        yi = y[key]

        # recurse through xi/yi
        is_equal, msg = deep_equals(xi, yi, return_msg=True)
        if not is_equal:
            return ret(False, f"[{key}]" + msg)

    return ret(True, "")


def _fh_equals_plugin(x, y, return_msg=False, deep_equals=None):
    """Test two forecasting horizons for equality.

    Correct if both x and y are ForecastingHorizon

    Parameters
    ----------
    x: ForcastingHorizon
    y: ForcastingHorizon
    return_msg : bool, optional, default=False
        whether to return informative message about what is not equal

    Returns
    -------
    is_equal: bool - True if x and y are equal in value
        x and y do not need to be equal in reference
    msg : str, only returned if return_msg = True
        indication of what is the reason for not being equal
            concatenation of the following strings:
            .is_relative - x is absolute and y is relative, or vice versa
            .values - values of x and y are not equal
    """
    if type(x).__name__ != "ForecastingHorizon":
        return None

    ret = _make_ret(return_msg)

    if x.is_relative != y.is_relative:
        return ret(False, ".is_relative")

    # recurse through values of x, y
    is_equal, msg = deep_equals(x._values, y._values, return_msg=True)
    if not is_equal:
        return ret(False, ".values" + msg)

    return ret(True, "")


def deep_equals_custom(x, y, return_msg=False, plugins=None):
    """Test two objects for equality in value.

    Correct if x/y are one of the following valid types:
        types compatible with != comparison
        pd.Series, pd.DataFrame, np.ndarray
        lists, tuples, or dicts of a valid type (recursive)

    Important note:
        this function will return "not equal" if types of x,y are different
        for instant, bool and numpy.bool are *not* considered equal

    Parameters
    ----------
    x : object
    y : object
    return_msg : bool, optional, default=False
        whether to return informative message about what is not equal
    plugins : list, optional, default=None
        list of plugins to use for custom deep_equals
        entries must be functions with the signature:
        ``(x, y, return_msg: bool) -> return``
        where return is:
        ``None``, if the plugin does not apply, otheriwse:
        ``is_equal: bool`` if ``return_msg=False``,
        ``(is_equal: bool, msg: str)`` if return_msg=True.
        Plugins can have an additional argument ``deep_equals=None``
        by which the parent function to be called recursively is passed

    Returns
    -------
    is_equal: bool - True if x and y are equal in value
        x and y do not need to be equal in reference
    msg : str, only returned if return_msg = True
        indication of what is the reason for not being equal
    """
    ret = _make_ret(return_msg)

    if type(x) is not type(y):
        return ret(False, f".type, x.type = {type(x)} != y.type = {type(y)}")

    # we now know all types are the same
    # so now we compare values

    # recursion through lists, tuples and dicts
    if isinstance(x, (list, tuple)):
        return ret(*_tuple_equals(x, y, return_msg=True))
    elif isinstance(x, dict):
        return ret(*_dict_equals(x, y, return_msg=True))
    elif _is_npnan(x):
        return ret(_is_npnan(y), f"type(x)={type(x)} != type(y)={type(y)}")
    elif isclass(x):
        return ret(x == y, f".class, x={x.__name__} != y={y.__name__}")

    if plugins is not None:
        for plugin in plugins:
            # check if plugin has deep_equals argument
            # if so, pass this function as argument to plugin
            # this allows for recursive calls to deep_equals

            # get the signature of the plugin
            sig = signature(plugin)
            # check if deep_equals is an argument of the plugin
            if "deep_equals" in sig.parameters:
                # we need to pass in the same plugins, so we curry
                def deep_equals_curried(x, y, return_msg=False):
                    return deep_equals_custom(
                        x, y, return_msg=return_msg, plugins=plugins
                    )

                kwargs = {"deep_equals": deep_equals_curried}
            else:
                kwargs = {}

            res = plugin(x, y, return_msg=return_msg, **kwargs)

            # if plugin does not apply, res is None
            if res is not None:
                return res

    # this if covers case where != is boolean
    # some types return a vector upon !=, this is covered in the next elif
    if isinstance(x == y, bool):
        return ret(x == y, f" !=, {x} != {y}")

    # check if numpy is available
    numpy_available = _softdep_available("numpy")
    if numpy_available:
        import numpy as np

    # deal with the case where != returns a vector
    if numpy_available and np.any(x != y) or any(_coerce_list(x != y)):
        return ret(False, f" !=, {x} != {y}")

    return ret(True, "")
