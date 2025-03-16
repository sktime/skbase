# -*- coding: utf-8 -*-
"""Tests for deep_equals utility."""
from copy import deepcopy

import pytest

from skbase.utils.deep_equals import deep_equals
from skbase.utils.dependencies import _check_soft_dependencies

# examples used for comparison below
EXAMPLES = [
    42,
    [],
    ((((())))),
    [[[[()]]]],
    3.5,
    4.2,
]

if _check_soft_dependencies("numpy", severity="none"):
    import numpy as np

    EXAMPLES += [
        np.array([2, 3, 4]),
        np.array([2, 4, 5]),
        np.array([2, 4, 5, 4]),
        np.nan,
        # these cases test that plugins are passed to recursions
        # in this case, the numpy equality plugin
        {"a": np.array([2, 3, 4]), "b": np.array([4, 3, 2])},
        [np.array([2, 3, 4]), np.array([4, 3, 2])],
        # test case to cover branch re dtype and equal_nan
        np.array([0.1, 1], dtype="object"),
        np.array([0.2, 1], dtype="object"),
        np.array([0.2, 1, 4], dtype="object"),
    ]

    # test cases with nested numpy arrays
    a = np.array(["a", "b"], dtype="object")
    a[0] = np.array([1, 2, 3])
    b = np.array(["a", "b", 42], dtype="object")
    b[1] = a
    EXAMPLES += [a, b]

if _check_soft_dependencies("pandas", severity="none"):
    import pandas as pd

    EXAMPLES += [
        pd.DataFrame({"a": [4, 2]}),
        pd.DataFrame({"a": [4, 3]}),
        pd.DataFrame({"a": [4, 3, 5]}),
        pd.DataFrame({"a": ["4", "3"]}),
        (np.array([1, 2, 4]), [pd.DataFrame({"a": [4, 2]})]),
        {"foo": [42], "bar": pd.Series([1, 2])},
        {"bar": [42], "foo": pd.Series([1, 2])},
        pd.Index([1, 2, 3]),
        pd.Index([2, 3, 4]),
        pd.Index([2, 3, 4, 6]),
        pd.Index([None]),
    ]

    # nested DataFrame example
    cols = [f"var_{i}" for i in range(2)]
    X = pd.DataFrame(columns=cols, index=[0, 1, 2])
    X["var_0"] = pd.Series(
        [pd.Series([1, 2, 3]), pd.Series([1, 2, 3]), pd.Series([1, 2, 3])]
    )

    X["var_1"] = pd.Series(
        [pd.Series([4, 5, 6]), pd.Series([4, 55, 6]), pd.Series([42, 5, 6])]
    )

    EXAMPLES += [X]

if _check_soft_dependencies("scikit-learn", severity="none"):
    from sklearn.ensemble import RandomForestRegressor

    EXAMPLES += [RandomForestRegressor()]
    EXAMPLES += [RandomForestRegressor(n_estimators=42)]


@pytest.mark.parametrize("fixture", EXAMPLES)
def test_deep_equals_positive(fixture):
    """Tests that deep_equals correctly identifies equal objects as equal."""
    x = copy_except_if_sklearn(fixture)
    y = copy_except_if_sklearn(fixture)

    msg = (
        f"deep_equals incorrectly returned False for two identical copies of "
        f"the following object: {x}"
    )
    assert deep_equals(x, y), msg


n = len(EXAMPLES)
DIFFERENT_PAIRS = [
    (EXAMPLES[i], EXAMPLES[j]) for i in range(n) for j in range(n) if i != j
]


@pytest.mark.parametrize("fixture1,fixture2", DIFFERENT_PAIRS)
def test_deep_equals_negative(fixture1, fixture2):
    """Tests that deep_equals correctly identifies unequal objects as unequal."""
    x = copy_except_if_sklearn(fixture1)
    y = copy_except_if_sklearn(fixture2)

    msg = (
        f"deep_equals incorrectly returned True when comparing "
        f"the following, different objects: x={x}, y={y}"
    )
    assert not deep_equals(x, y), msg


def copy_except_if_sklearn(obj):
    """Copy obj if it is not a scikit-learn estimator.

    We use this function as deep_copy should return True for
    identical sklearn estimators, but False for different copies.

    This is the current status quo, possibly we want to change this in the future.
    """
    if not _check_soft_dependencies("scikit-learn", severity="none"):
        return deepcopy(obj)
    else:
        from sklearn.base import BaseEstimator

        if isinstance(obj, BaseEstimator):
            return obj
        else:
            return deepcopy(obj)
