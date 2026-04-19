# -*- coding: utf-8 -*-
"""Common functionality for skbase unit tests."""

from typing import List

from skbase.base import BaseEstimator, BaseObject

__all__: List[str] = [
    "SKBASE_BASE_CLASSES",
]
__author__: List[str] = ["fkiraly", "RNKuhns"]

SKBASE_BASE_CLASSES = (BaseObject, BaseEstimator)


# Fixture class for testing tag system
class Parent(BaseObject):
    """Parent class to test BaseObject's usage."""

    _tags = {"A": "1", "B": 2, "C": 1234, "3": "D"}

    def __init__(self, a="something", b=7, c=None):
        """Initialize the class."""
        self.a = a
        self.b = b
        self.c = c
        super().__init__()

    def some_method(self):
        """To be implemented by child class."""
        pass


# Fixture class for testing tag system, child overrides tags
class Child(Parent):
    """Child class that is child of FixtureClassParent."""

    _tags = {"A": 42, "3": "E"}
    __author__ = ["fkiraly", "RNKuhns"]

    def some_method(self):
        """Child class' implementation."""
        pass

    def some_other_method(self):
        """To be implemented in the child class."""
        pass


# Fixture class for testing tag system, child overrides tags
class ClassWithABTrue(Parent):
    """Child class that sets A, B tags to True."""

    _tags = {"A": True, "B": True}
    __author__ = ["fkiraly", "RNKuhns"]

    def some_method(self):
        """Child class' implementation."""
        pass

    def some_other_method(self):
        """To be implemented in the child class."""
        pass
