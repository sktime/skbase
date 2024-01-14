#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests of the functionality for miscellaneous utilities.

tests in this module include:

- test_subset_dict_keys_output: verify that subset_dict_keys outputs expected format.
"""
from skbase.utils import subset_dict_keys

__author__ = ["RNKuhns"]


def test_subset_dict_keys_output():
    """Test subset_dict_keys outputs expected result."""
    some_dict = {"some_param__a": 1, "some_param__b": 2, "some_param__c": 3}

    assert subset_dict_keys(some_dict, "some_param__a") == {"some_param__a": 1}

    assert subset_dict_keys(some_dict, ("some_param__a", "some_param__b")) == {
        "some_param__a": 1,
        "some_param__b": 2,
    }

    assert subset_dict_keys(some_dict, ("a", "b"), prefix="some_param") == {
        "a": 1,
        "b": 2,
    }

    assert subset_dict_keys(
        some_dict, ("a", "b"), prefix="some_param", remove_prefix=False
    ) == {"some_param__a": 1, "some_param__b": 2}

    assert subset_dict_keys(
        some_dict, (c for c in ("some_param__a", "some_param__b"))
    ) == {"some_param__a": 1, "some_param__b": 2}
