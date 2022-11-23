# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for skbase lookup functionality.

tests in this module:

    test_get_class_tags  - tests get_class_tags inheritance logic
    test_get_class_tag   - tests get_class_tag logic, incl default value
    test_get_tags        - tests get_tags inheritance logic
    test_get_tag         - tests get_tag logic, incl default value
    test_set_tags        - tests set_tags logic and related get_tags inheritance

    test_reset           - tests reset logic on a simple, non-composite estimator
    test_reset_composite - tests reset logic on a composite estimator
"""
from typing import List

from skbase.lookup._lookup import _is_non_public_module

# import pytest


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
