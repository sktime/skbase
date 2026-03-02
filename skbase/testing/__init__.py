# -*- coding: utf-8 -*-
""":mod:`skbase.testing` provides a framework to test ``BaseObject``-s."""

from skbase.testing.test_all_objects import (
    BaseFixtureGenerator,
    QuickTester,
    TestAllObjects,
)

__all__: list[str] = ["BaseFixtureGenerator", "QuickTester", "TestAllObjects"]
__author__: list[str] = ["fkiraly"]
