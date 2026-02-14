# -*- coding: utf-8 -*-
"""Common functionality for skbase unit tests."""

from typing import List

from skbase.base import BaseEstimator, BaseObject

__all__: List[str] = [
    "SKBASE_BASE_CLASSES",
    "SKBASE_MODULES",
    "SKBASE_PUBLIC_MODULES",
]
__author__: List[str] = ["fkiraly", "RNKuhns"]

# bug 442 fixed: metaclasses now discovered correctly on all Python versions
IMPORT_CLS = ("CommonMagicMeta", "MagicAttribute")

SKBASE_BASE_CLASSES = (BaseObject, BaseEstimator)
SKBASE_MODULES = (
    "skbase",
    "skbase._exceptions",
    "skbase._nopytest_tests",
    "skbase.base",
    "skbase.base._base",
    "skbase.base._clone_base",
    "skbase.base._clone_plugins",
    "skbase.base._meta",
    "skbase.base._pretty_printing",
    "skbase.base._pretty_printing._object_html_repr",
    "skbase.base._pretty_printing._pprint",
    "skbase.base._tagmanager",
    "skbase.lookup",
    "skbase.lookup.tests",
    "skbase.lookup.tests.test_lookup",
    "skbase.lookup._lookup",
    "skbase.testing",
    "skbase.testing.test_all_objects",
    "skbase.testing.utils",
    "skbase.testing.utils._conditional_fixtures",
    "skbase.testing.utils.inspect",
    "skbase.testing.utils.tests",
    "skbase.testing.utils.tests.test_deep_equals",
    "skbase.tests",
    "skbase.tests.conftest",
    "skbase.tests.test_base",
    "skbase.tests.test_baseestimator",
    "skbase.tests.mock_package.test_mock_package",
    "skbase.utils",
    "skbase.utils._check",
    "skbase.utils._iter",
    "skbase.utils._nested_iter",
    "skbase.utils._utils",
    "skbase.utils.deep_equals",
    "skbase.utils.deep_equals._common",
    "skbase.utils.deep_equals._deep_equals",
    "skbase.utils.dependencies",
    "skbase.utils.dependencies._dependencies",
    "skbase.utils.dependencies._import",
    "skbase.utils.doctest_run",
    "skbase.utils.git_diff",
    "skbase.utils.random_state",
    "skbase.utils.stderr_mute",
    "skbase.utils.stdout_mute",
    "skbase.validate",
    "skbase.validate._named_objects",
    "skbase.validate._types",
)
SKBASE_PUBLIC_MODULES = (
    "skbase",
    "skbase.base",
    "skbase.lookup",
    "skbase.lookup.tests",
    "skbase.lookup.tests.test_lookup",
    "skbase.testing",
    "skbase.testing.test_all_objects",
    "skbase.testing.utils",
    "skbase.testing.utils.inspect",
    "skbase.testing.utils.tests",
    "skbase.testing.utils.tests.test_deep_equals",
    "skbase.tests",
    "skbase.tests.conftest",
    "skbase.tests.test_base",
    "skbase.tests.test_baseestimator",
    "skbase.tests.mock_package.test_mock_package",
    "skbase.utils",
    "skbase.utils.deep_equals",
    "skbase.utils.dependencies",
    "skbase.utils.doctest_run",
    "skbase.utils.git_diff",
    "skbase.utils.random_state",
    "skbase.utils.stderr_mute",
    "skbase.utils.stdout_mute",
    "skbase.validate",
)


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
