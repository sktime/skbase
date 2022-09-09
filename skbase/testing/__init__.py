# -*- coding: utf-8 -*-
""":mod:`baseobject.testing` provides a framework to test ``BaseObjects``."""
from typing import List

from baseobject.testing.test_all_objects import (
    BaseFixtureGenerator,
    QuickTester,
    TestAllObjects,
)

__all__: List[str] = ["BaseFixtureGenerator", "QuickTester", "TestAllObjects"]
__author__: List[str] = ["fkiraly"]
