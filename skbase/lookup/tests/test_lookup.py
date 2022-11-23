# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for skbase lookup functionality.

tests in this module:

    test_is_non_public_module  - tests _is_non_public_module logic
"""
from typing import List

import pandas as pd
import pytest

from skbase import BaseObject
from skbase.lookup._lookup import (
    _filter_by_class,
    _is_ignored_module,
    _is_non_public_module,
    all_objects,
)
from skbase.mock_package.mock_package import (
    AnotherClass,
    CompositionDummy,
    InheritsFromBaseObject,
)

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = []


MOD_NAMES = {
    "public": ("skbase", "skbase.lookup", "some_module.some_sub_module"),
    "non_public": (
        "skbase.lookup._lookup",
        "some_module._some_non_public_sub_module",
        "_skbase",
    ),
}


def test_is_non_public_module():
    """Test _is_non_public_module correctly indentifies non-public modules."""
    for mod in MOD_NAMES["public"]:
        assert _is_non_public_module(mod) is False
    for mod in MOD_NAMES["non_public"]:
        assert _is_non_public_module(mod) is True


def test_is_non_public_module_raises_error():
    """Test _is_non_public_module raises a ValueError for non-string input."""
    with pytest.raises(ValueError):
        _is_non_public_module(7)


def test_is_ignored_module():
    """Test _is_ignored_module correctly identifies modules in ignored sequence."""
    # Test case when no modules are ignored
    for mod in MOD_NAMES["public"]:
        assert _is_ignored_module(mod) is False

    # No modules should be flagged as ignored if the ignored moduels aren't encountered
    modules_to_ignore = ("a_module_not_encountered",)
    for mod in MOD_NAMES["public"]:
        assert _is_ignored_module(mod, modules_to_ignore=modules_to_ignore) is False

    # When ignored modules are encountered then they should be flagged as True
    modules_to_ignore = ("skbase",)
    for mod in MOD_NAMES["public"]:
        if "skbase" in mod:
            expected_to_ignore = True
        else:
            expected_to_ignore = False
        assert (
            _is_ignored_module(mod, modules_to_ignore=modules_to_ignore)
            is expected_to_ignore
        )


def test_filter_by_class():
    """Test _filter_by_class correctly identifies classes."""
    # Test case when no class filter is applied (should always return True)
    assert _filter_by_class(CompositionDummy) is True

    # Test case where a signle filter is applied
    assert _filter_by_class(CompositionDummy, BaseObject) is True
    assert _filter_by_class(CompositionDummy, InheritsFromBaseObject) is False

    # Test case when sequence of classes supplied as filter
    assert (
        _filter_by_class(CompositionDummy, (BaseObject, InheritsFromBaseObject)) is True
    )
    assert (
        _filter_by_class(CompositionDummy, (AnotherClass, InheritsFromBaseObject))
        is False
    )


@pytest.mark.parametrize("as_dataframe", [True, False])
@pytest.mark.parametrize("return_names", [True, False])
def test_all_objects_returns_expected_types(as_dataframe, return_names):
    """Check that all_objects return argument has correct type."""
    objs = all_objects(
        package_name="skbase.mock_package",
        return_names=return_names,
        as_dataframe=as_dataframe,
    )
    # We expect at least one object to be returned
    assert len(objs) > 0

    if as_dataframe:
        expected_columns = 2 if return_names else 1
        assert isinstance(objs, pd.DataFrame) and objs.shape[1] == expected_columns
        # Verify all objects in the object columns are BaseObjects
        for i in range(len(objs)):
            expected_obj_column = 1 if return_names else 0
            assert issubclass(objs.iloc[i, expected_obj_column], BaseObject)
            if return_names:
                # Value in name column should be a string
                assert isinstance(objs.iloc[i, 0], str)
                # Value in name column should be name of object in object column
                assert objs.iloc[i, 0] == objs.iloc[i, 1].__name__

    else:
        # Should return a list
        assert isinstance(objs, list)
        # checks return type specification (see docstring)
        if return_names:
            for obj in objs:
                assert issubclass(obj[1], BaseObject)
                if return_names:
                    assert isinstance(obj, tuple) and len(obj) == 2
                    assert isinstance(obj[0], str)
                    assert obj[0] == obj[1].__name__
