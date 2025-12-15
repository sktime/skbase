# -*- coding: utf-8 -*-
"""Mock package for skbase testing.

This package contains controlled test fixtures used by lookup tests.
"""
from typing import List

from .test_fixtures import Child, ClassWithABTrue, Parent
from .test_mock_package import (
    MOCK_PACKAGE_OBJECTS,
    AnotherClass,
    CompositionDummy,
    InheritsFromBaseObject,
    NotABaseObject,
)

__all__: List[str] = [
    "MOCK_PACKAGE_OBJECTS",
]

__author__: List[str] = ["fkiraly", "RNKuhns"]
