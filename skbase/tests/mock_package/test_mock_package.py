# -*- coding: utf-8 -*-
"""Mock package for testing skbase functionality."""
from copy import deepcopy
from typing import List

from skbase.base import BaseObject

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
]
