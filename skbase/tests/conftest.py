# -*- coding: utf-8 -*-
"""Common functionality for skbase unit tests."""
from copy import deepcopy
from typing import List

from skbase.base import BaseObject

__all__: List[str] = [
    "FixtureClassParent",
    "FixtureClassChild",
    "CompositionDummy",
    "ResetTester",
    "InvalidInitSignatureTester",
    "RequiredParam",
    "Buggy",
    "ModifyParam",
    "NoParamInterface",
]
__author__: List[str] = ["RNKuhns"]


# Fixture class for testing tag system
class FixtureClassParent(BaseObject):
    """Fixture class to test BaseObject's usage."""

    _tags = {"A": "1", "B": 2, "C": 1234, 3: "D"}

    def __init__(self, a="something", b=7, c=None):
        self.a = a
        self.b = b
        self.c = c
        super().__init__()

    def some_method(self):
        """To be implemented by child class."""
        pass


# Fixture class for testing tag system, child overrides tags
class FixtureClassChild(FixtureClassParent):
    """Fixture class that is child of FixtureClassParent."""

    _tags = {"A": 42, 3: "E"}
    __author__ = ["RNKuhns"]

    def some_method(self):
        """Child class' implementation."""
        pass

    def some_other_method(self):
        """To be implemented in the child class."""
        pass


# Test composition related interface functionality
class CompositionDummy(BaseObject):
    """Potentially composite object, for testing."""

    def __init__(self, foo, bar=84):
        self.foo = foo
        self.foo_ = deepcopy(foo)
        self.bar = bar
        super().__init__()


class ResetTester(BaseObject):
    """Class for testing reset functionality."""

    clsvar = 210

    def __init__(self, a, b=42):
        self.a = a
        self.b = b
        self.c = 84
        super().__init__()

    def foo(self, d=126):
        """Foo gets done."""
        self.d = deepcopy(d)
        self._d = deepcopy(d)
        self.d_ = deepcopy(d)
        self.f__o__o = 252


class InvalidInitSignatureTester(BaseObject):
    """Class for testing invalid signature."""

    def __init__(self, a, *args):
        super().__init__()


class RequiredParam(BaseObject):
    """BaseObject class with _required_parameters."""

    _required_parameters = ["a"]

    def __init__self(self, a, b=7):
        self.a = a
        self.b = b
        super().__init__()


class Buggy(BaseObject):
    """A buggy BaseObject that does not set its parameters right."""

    def __init__(self, a=None):
        self.a = 1
        self._a = a
        super().__init__()


class ModifyParam(BaseObject):
    """A non-conforming BaseObject that modifyies parameters in init."""

    def __init__(self, a=7):
        self.a = deepcopy(a)
        super().__init__()


class NoParamInterface:
    """Simple class without BaseObject's param interface for testing get_params."""

    def __init__(self, a=7, b=12):
        self.a = a
        self.b = b
        super().__init__()
