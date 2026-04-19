# -*- coding: utf-8 -*-
"""Mock package for testing skbase functionality."""

from copy import deepcopy
from typing import List

from skbase.base import BaseObject

from .test_fixtures import Child, ClassWithABTrue, Parent

__all__: List[str] = [
    "CompositionDummy",
    "InheritsFromBaseObject",
    "AnotherClass",
    "NotABaseObject",
]
__author__: List[str] = ["fkiraly", "RNKuhns"]


class CompositionDummy(BaseObject):
    """Potentially composite object, for testing."""

    def __init__(self, foo, bar=84):
        self.foo = foo
        self.foo_ = deepcopy(foo)
        self.bar = bar

        super(CompositionDummy, self).__init__()

    @classmethod
    def get_test_params(cls, parameter_set="default"):
        """Return testing parameter settings for the estimator.

        Parameters
        ----------
        parameter_set : str, default="default"
            Name of the set of test parameters to return, for use in tests. If no
            special parameters are defined for a value, will return `"default"` set.

        Returns
        -------
        params : dict or list of dict, default = {}
            Parameters to create testing instances of the class
            Each dict are parameters to construct an "interesting" test instance, i.e.,
            `MyClass(**params)` or `MyClass(**params[i])` creates a valid test instance.
            `create_test_instance` uses the first (or only) dictionary in `params`
        """
        params1 = {"foo": 42}
        params2 = {"foo": CompositionDummy(126)}
        return [params1, params2]


class InheritsFromBaseObject(BaseObject):
    """A class inheriting from BaseObject."""


class AnotherClass(BaseObject):
    """Another class inheriting from BaseObject."""


class NotABaseObject:
    """A class that is not a BaseObject."""

    def __init__(self, a=7):
        self.a = a


class _NonPublicClass(BaseObject):
    """A nonpublic class inheriting from BaseObject."""


MOCK_PACKAGE_OBJECTS = [
    AnotherClass,
    CompositionDummy,
    InheritsFromBaseObject,
    _NonPublicClass,
    Parent,
    Child,
    ClassWithABTrue,
]

# Expected public classes by module for validation
MOCK_PACKAGE_PUBLIC_CLASSES_BY_MODULE = {
    "skbase.tests.mock_package._private_pkg.test_module": ("PrivateModuleClass",),
    "skbase.tests.mock_package.test_mock_package": (
        "AnotherClass",
        "CompositionDummy",
        "InheritsFromBaseObject",
        "NotABaseObject",
    ),
    "skbase.tests.mock_package.test_fixtures": (
        "Child",
        "ClassWithABTrue",
        "Parent",
    ),
}

# Expected all classes by module (including non-public) for validation
MOCK_PACKAGE_CLASSES_BY_MODULE = {
    "skbase.tests.mock_package._private_pkg.test_module": (
        "PrivateModuleClass",
        "_PrivateModuleHiddenClass",
    ),
    "skbase.tests.mock_package.test_mock_package": (
        "AnotherClass",
        "CompositionDummy",
        "InheritsFromBaseObject",
        "NotABaseObject",
        "_NonPublicClass",
    ),
    "skbase.tests.mock_package.test_fixtures": (
        "Child",
        "ClassWithABTrue",
        "Parent",
    ),
    "skbase.tests.mock_package.test_private_module": ("_PrivateThing",),
}

# Expected public functions by module for validation
MOCK_PACKAGE_PUBLIC_FUNCTIONS_BY_MODULE = {
    "skbase.tests.mock_package._private_pkg.test_module": (
        "private_module_public_function",
    ),
    "skbase.tests.mock_package.test_module_public": (
        "decorated_function",
        "my_decorator",
        "simple_function",
    ),
    "skbase.tests.mock_package.subpkg.test_module_b": ("subpkg_fn",),
}

# Expected all functions by module (including non-public) for validation
MOCK_PACKAGE_FUNCTIONS_BY_MODULE = {
    "skbase.tests.mock_package._private_pkg.test_module": (
        "private_module_public_function",
        "_private_module_hidden_function",
    ),
    "skbase.tests.mock_package.test_module_public": (
        "decorated_function",
        "_private_helper",
        "my_decorator",
        "simple_function",
    ),
    "skbase.tests.mock_package.subpkg.test_module_b": ("subpkg_fn",),
}

# List of all public modules in mock package
MOCK_PACKAGE_PUBLIC_MODULES = (
    "skbase.tests.mock_package",
    "skbase.tests.mock_package.subpkg",
    "skbase.tests.mock_package.subpkg.test_module_b",
    "skbase.tests.mock_package.test_fixtures",
    "skbase.tests.mock_package.test_mock_package",
    "skbase.tests.mock_package.test_module_public",
    "skbase.tests.mock_package.test_private_module",
)

# List of all modules (including non-public) in mock package
MOCK_PACKAGE_MODULES = (
    "skbase.tests.mock_package",
    "skbase.tests.mock_package._private_pkg",
    "skbase.tests.mock_package._private_pkg.test_module",
    "skbase.tests.mock_package.subpkg",
    "skbase.tests.mock_package.subpkg.test_module_b",
    "skbase.tests.mock_package.test_fixtures",
    "skbase.tests.mock_package.test_mock_package",
    "skbase.tests.mock_package.test_module_public",
    "skbase.tests.mock_package.test_private_module",
)
