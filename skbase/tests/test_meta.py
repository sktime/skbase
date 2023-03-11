# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for BaseMetaObject and BaseMetaEstimator mixins.

tests in this module:


"""

__author__ = ["RNKuhns"]
import pytest

from skbase.base import BaseEstimator, BaseObject
from skbase.base._meta import BaseMetaEstimator, BaseMetaObject


class SomeClass(BaseObject):
    """Some class for testing."""

    def __init__(self, z=12):
        self.z = z


class SomeEstimator(BaseEstimator):
    """Some class for testing."""

    def __init__(self, y=32):
        self.y = y


class MetaObjectTester(BaseMetaObject):
    """Class to test meta object functionality."""

    def __init__(self, a=7, b="something", c=None, steps=None):
        self.a = a
        self.b = b
        self.c = c
        self.steps = steps


class MetaEstimatorTester(BaseMetaEstimator):
    """Class to test meta estimator functionality."""

    def __init__(self, a=7, b="something", c=None, steps=None):
        self.a = a
        self.b = b
        self.c = c
        self.steps = steps


@pytest.fixture
def fixture_meta_object():
    return MetaObjectTester()


@pytest.fixture
def fixture_meta_estimator():
    return MetaEstimatorTester()


def test_is_composit_returns_true(fixture_meta_object, fixture_meta_estimator):
    """Test that `is_composite` method returns True."""
    msg = "`is_composite` should always be True for subclasses of "
    assert fixture_meta_object.is_composite() is True, msg + "`BaseMetaObject`."
    assert fixture_meta_estimator.is_composite() is True, msg + "`BaseMetaEstimator`."
