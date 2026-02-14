# -*- coding: utf-8 -*-
"""Additional fixture classes for the mock package used in lookup tests."""

from typing import List

from skbase.base import BaseObject

__author__: List[str] = ["fkiraly", "RNKuhns"]


class Parent(BaseObject):
    """Parent class to test tag inheritance and class filters."""

    _tags = {"A": "1", "B": 2, "C": 1234, "3": "D"}

    def __init__(self, a="something", b=7, c=None):
        """Initialize the fixture with simple attributes."""
        self.a = a
        self.b = b
        self.c = c
        super().__init__()

    def some_method(self):
        """Placeholder method used in tests."""
        pass


class Child(Parent):
    """Child class that overrides some tags."""

    _tags = {"A": 42, "3": "E"}
    __author__ = ["fkiraly", "RNKuhns"]

    def some_method(self):
        """Child placeholder method used in tests."""
        pass


class ClassWithABTrue(Parent):
    """Child class that sets A and B tags to True."""

    _tags = {"A": True, "B": True}
    __author__ = ["fkiraly", "RNKuhns"]

    def some_method(self):
        """Placeholder method used in tests."""
        pass
