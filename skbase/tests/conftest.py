# -*- coding: utf-8 -*-
"""Common functionality for skbase unit tests."""
from copy import deepcopy
from typing import List

from skbase.base import BaseEstimator, BaseObject

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
__author__: List[str] = ["fkiraly", "RNKuhns"]

SKBASE_BASE_CLASSES = (BaseObject, BaseEstimator)
SKBASE_MODULES = (
    "skbase",
    "skbase._exceptions",
    "skbase.base",
    "skbase.base._base",
    "skbase.base._meta",
    "skbase.lookup",
    "skbase.lookup._lookup",
    "skbase.mock_package",
    "skbase.mock_package.mock_package",
    "skbase.testing",
    "skbase.testing.test_all_objects",
    "skbase.testing.utils",
    "skbase.testing.utils._conditional_fixtures",
    "skbase.testing.utils._dependencies",
    "skbase.testing.utils.deep_equals",
    "skbase.testing.utils.inspect",
    "skbase.utils",
    "skbase.utils._nested_iter",
    "skbase.validate",
    "skbase.validate._types",
)
SKBASE_PUBLIC_MODULES = (
    "skbase",
    "skbase.base",
    "skbase.lookup",
    "skbase.mock_package",
    "skbase.mock_package.mock_package",
    "skbase.testing",
    "skbase.testing.test_all_objects",
    "skbase.testing.utils",
    "skbase.testing.utils.deep_equals",
    "skbase.testing.utils.inspect",
    "skbase.utils",
    "skbase.validate",
)
SKBASE_PUBLIC_CLASSES_BY_MODULE = {
    "skbase": ("BaseEstimator", "BaseMetaEstimator", "BaseObject"),
    "skbase._exceptions": ("FixtureGenerationError", "NotFittedError"),
    "skbase.base": ("BaseEstimator", "BaseMetaEstimator", "BaseObject"),
    "skbase.base._base": ("BaseEstimator", "BaseObject"),
    "skbase.base._meta": ("BaseMetaEstimator",),
    "skbase.lookup._lookup": ("ClassInfo", "FunctionInfo", "ModuleInfo"),
    "skbase.testing": ("BaseFixtureGenerator", "QuickTester", "TestAllObjects"),
    "skbase.testing.test_all_objects": (
        "BaseFixtureGenerator",
        "QuickTester",
        "TestAllObjects",
    ),
}
SKBASE_CLASSES_BY_MODULE = SKBASE_PUBLIC_CLASSES_BY_MODULE.copy()
SKBASE_CLASSES_BY_MODULE.update(
    {
        "skbase": (
            "BaseEstimator",
            "BaseMetaEstimator",
            "BaseObject",
            "_HeterogenousMetaEstimator",
        ),
        "skbase.base._meta": ("BaseMetaEstimator", "_HeterogenousMetaEstimator"),
    }
)
SKBASE_PUBLIC_FUNCTIONS_BY_MODULE = {
    "skbase": ("all_objects", "get_package_metadata"),
    "skbase._exceptions": (),
    "skbase.base": (),
    "skbase.base._base": (),
    "skbase.base._meta": (),
    "skbase.lookup": ("all_objects", "get_package_metadata"),
    "skbase.lookup._lookup": ("all_objects", "get_package_metadata"),
    "skbase.testing": (),
    "skbase.testing.utils._dependencies": (),
    "skbase.testing.test_all_objects": (),
    "skbase.testing.utils": (),
    "skbase.testing.utils._conditional_fixtures": (
        "create_conditional_fixtures_and_names",
    ),
    "skbase.testing.utils.deep_equals": ("deep_equals",),
    "skbase.testing.utils.inspect": (),
    "skbase.validate": (),
    "skbase.utils": ("flatten", "is_flat", "unflat_len", "unflatten"),
    "skbase.utils._nested_iter": (
        "flatten",
        "is_flat",
        "unflat_len",
        "unflatten",
    ),
    "skbase.validate.types": (),
}
SKBASE_FUNCTIONS_BY_MODULE = SKBASE_PUBLIC_FUNCTIONS_BY_MODULE.copy()
SKBASE_FUNCTIONS_BY_MODULE.update(
    {
        "skbase.lookup._lookup": (
            "_determine_module_path",
            "_get_return_tags",
            "_is_ignored_module",
            "all_objects",
            "_is_non_public_module",
            "get_package_metadata",
            "_make_dataframe",
            "_walk",
            "_filter_by_tags",
            "_filter_by_class",
            "_import_module",
            "_check_object_types",
            "_get_module_info",
        ),
        "skbase.testing.utils._dependencies": (
            "_check_soft_dependencies",
            "_check_python_version",
        ),
        "skbase.testing.utils.deep_equals": (
            "_pandas_equals",
            "_dict_equals",
            "_is_pandas",
            "_tuple_equals",
            "_fh_equals",
            "deep_equals",
        ),
        "skbase.testing.utils.inspect": ("_get_args",),
        "skbase.utils._nested_iter": (
            "_remove_single",
            "flatten",
            "is_flat",
            "unflat_len",
            "unflatten",
        ),
        "skbase.validate._types": (
            "_check_iterable_of_class_or_error",
            "_check_list_of_str",
            "_check_list_of_str_or_error",
        ),
    }
)


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
    __author__ = ["fkiraly", "RNKuhns"]

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

    def __init__(self, a, b=7):
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


class _NonPublicClass(BaseObject):
    """A nonpublic class inheritting from BaseObject."""


class NotABaseObject:
    """A class that is not a BaseObject."""

    def __init__(self, a=7):
        self.a = a


SKBASE_TEST_CLASSES = [
    FixtureClassParent,
    FixtureClassChild,
    CompositionDummy,
    ResetTester,
    InvalidInitSignatureTester,
    RequiredParam,
    Buggy,
    ModifyParam,
    NoParamInterface,
]
