# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for BaseMetaObject and BaseMetaEstimator mixins.

tests in this module:


"""

__author__ = ["RNKuhns"]
# import pytest

from skbase.base import BaseObject
from skbase.base._meta import BaseMetaObject


class SomeClass(BaseObject):
    """Some class for testing."""

    def __init__(self, z=None):
        self.z = z


class MetaObjectTester(BaseMetaObject, BaseObject):
    """Class to test meta object functionality."""

    _steps_attr = "some_step_attr"

    def __init__(self, a=7, b="something", c=None, some_step_attr=None):
        self.a = a
        self.b = b
        self.c = c
        self.some_step_attr = some_step_attr
