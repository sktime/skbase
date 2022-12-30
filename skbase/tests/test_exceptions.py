# -*- coding: utf-8 -*-
"""Tests for skbase exceptions.

tests in this module:

    test_baseestimator_inheritance - Test BaseEstimator inherits from BaseObject.
    test_has_is_fitted - Test that BaseEstimator has is_fitted interface.
    test_has_check_is_fitted - Test that BaseEstimator has check_is_fitted inteface.
    test_is_fitted  - Test that is_fitted property returns _is_fitted as expected.
    test_check_is_fitted_raises_error_when_unfitted - Test check_is_fitted raises error.
"""
from typing import List

import pytest

from skbase._exceptions import FixtureGenerationError, NotFittedError

__author__: List[str] = ["fkiraly", "RNKuhns"]

ALL_EXCEPTIONS = [FixtureGenerationError, NotFittedError]


@pytest.mark.parametrize("skbase_exception", ALL_EXCEPTIONS)
def test_exceptions_raise_error(skbase_exception):
    """Test that skbase exceptions raise an error as expected."""
    with pytest.raises(skbase_exception):
        raise skbase_exception()
