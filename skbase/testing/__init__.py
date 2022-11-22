# -*- coding: utf-8 -*-
""":mod:`skbase.testing` provides a framework to test ``BaseObject``-s."""
from typing import List

from skbase.testing.test_all_objects import (
    BaseFixtureGenerator,
    QuickTester,
    TestAllObjects,
)

__all__: List[str] = ["BaseFixtureGenerator", "QuickTester", "TestAllObjects"]
__author__: List[str] = ["fkiraly"]
