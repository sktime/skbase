# -*- coding: utf-8 -*-
"""Tests for skbase exceptions.

tests in this module:

    test_exceptions_raise_error - Test that skbase exceptions raise expected error.
"""
from typing import List

import pytest

from skbase._exceptions import FixtureGenerationError, NotFittedError

__author__: List[str] = ["RNKuhns"]

ALL_EXCEPTIONS = [FixtureGenerationError, NotFittedError]


@pytest.mark.parametrize("skbase_exception", ALL_EXCEPTIONS)
def test_exceptions_raise_error(skbase_exception):
    """Test that skbase exceptions raise an error as expected."""
    with pytest.raises(skbase_exception):
        raise skbase_exception()
