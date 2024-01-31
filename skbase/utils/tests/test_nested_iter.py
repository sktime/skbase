#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests of the functionality for working with iterables.

tests in this module include:

- test_remove_single
- test_flatten
- test_unflatten
- test_unflat_len
- test_is_flat
"""
# import pytest

from skbase.base import BaseEstimator, BaseObject
from skbase.utils._nested_iter import (
    _remove_single,
    flatten,
    is_flat,
    unflat_len,
    unflatten,
)

__author__ = ["RNKuhns"]


def test_remove_single():
    """Test _remove_single output is as expected."""
    # Verify that length > 1 sequence not impacted.
    assert _remove_single([1, 2, 3]) == [1, 2, 3]

    # Verify single member of sequence is removed as expected
    assert _remove_single([1]) == 1


def test_flatten():
    """Test flatten output is as expected."""
    assert flatten([1, 2, [3, (4, 5)], 6]) == [1, 2, 3, 4, 5, 6]

    # Verify functionality with classes and objects
    assert flatten((BaseObject, 7, (BaseObject, BaseEstimator))) == (
        BaseObject,
        7,
        BaseObject,
        BaseEstimator,
    )
    assert flatten((BaseObject(), 7, (BaseObject, BaseEstimator()))) == (
        BaseObject(),
        7,
        BaseObject,
        BaseEstimator(),
    )


def test_unflatten():
    """Test output of unflatten."""
    assert unflatten([1, 2, 3, 4, 5, 6], [6, 3, [5, (2, 4)], 1]) == [
        1,
        2,
        [3, (4, 5)],
        6,
    ]


def test_unflat_len():
    """Test output of unflat_len."""
    assert unflat_len(7) == 1
    assert unflat_len((1, 2)) == 2
    assert unflat_len([1, (2, 3), 4, 5]) == 5
    assert unflat_len([1, 2, (c for c in (2, 3, 4))]) == 5
    assert unflat_len((c for c in [1, 2, (c for c in (2, 3, 4))])) == 5


def test_is_flat():
    """Test output of is_flat."""
    assert is_flat([1, 2, 3, 4, 5]) is True
    assert is_flat([1, (2, 3), 4, 5]) is False
    # Check with flat generator
    assert is_flat((c for c in [1, 2, 3])) is True
    # Check with nested generator
    assert is_flat([1, 2, (c for c in (2, 3, 4))]) is False
    # Check with generator nested in a generator
    assert is_flat((c for c in [1, 2, (c for c in (2, 3, 4))])) is False
