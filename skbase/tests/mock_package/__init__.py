# -*- coding: utf-8 -*-
"""Mock package for skbase testing."""

from typing import List

from .test_fixtures import Child  # noqa: F401
from .test_fixtures import ClassWithABTrue  # noqa: F401
from .test_fixtures import Parent  # noqa: F401
from .test_mock_package import MOCK_PACKAGE_OBJECTS  # noqa: F401
from .test_mock_package import AnotherClass  # noqa: F401
from .test_mock_package import CompositionDummy  # noqa: F401
from .test_mock_package import InheritsFromBaseObject  # noqa: F401
from .test_mock_package import NotABaseObject  # noqa: F401

__all__: List[str] = [
    "MOCK_PACKAGE_OBJECTS",
]

__author__: List[str] = ["fkiraly", "RNKuhns"]
