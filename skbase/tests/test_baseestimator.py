# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for BaseEstimator class.

tests in this module:

    test_has_is_fitted - Test that BaseEstimator has is_fitted interface
    test_has_check_is_fitted - Test that BaseEstimator has check_is_fitted inteface.
    test_is_fitted  - Test that is_fitted property returns _is_fitted as expected.
    test_check_is_fitted   - Test that check_is_fitted works as expected.
"""

__author__ = ["fkiraly"]
import inspect

import pytest

from skbase import BaseEstimator, BaseObject
from skbase._exceptions import NotFittedError


# Fixture class for testing simple fittable estimator
class FixtureSimpleFittableEstimator(BaseEstimator):
    """Fittable estimator for testing."""

    def fit(self):
        """Fit method for testing."""
        self._is_fitted = True


@pytest.fixture
def fixture_estimator_instance():
    """Pytest fixture of BaseEstimator instance."""
    return FixtureSimpleFittableEstimator()


def test_baseestimator_inheritance():
    """Check BaseEstimator correctly inherits from BaseObject."""
    estimator_is_subclass_of_baseobejct = issubclass(BaseEstimator, BaseObject)
    estimator_instance_is_baseobject_instance = isinstance(BaseEstimator(), BaseObject)
    assert (
        estimator_is_subclass_of_baseobejct
        and estimator_instance_is_baseobject_instance
    ), "`BaseEstimator` does not correctly inherit from `BaseObject`."


def test_has_is_fitted(fixture_estimator_instance):
    """Test BaseEstimator has `is_fitted` property."""
    has_private_is_fitted = hasattr(fixture_estimator_instance, "_is_fitted")
    has_is_fitted = hasattr(fixture_estimator_instance, "is_fitted")
    assert (
        has_private_is_fitted and has_is_fitted
    ), "BaseEstimator does not have `is_fitted` property;"


def test_has_check_is_fitted(fixture_estimator_instance):
    """Test BaseEstimator has `check_is_fitted` method."""
    has_check_is_fitted = hasattr(fixture_estimator_instance, "check_is_fitted")
    is_method = inspect.ismethod(fixture_estimator_instance.check_is_fitted)
    assert (
        has_check_is_fitted and is_method
    ), "`BaseEstimator` does not have `check_is_fitted` method."


def test_is_fitted(fixture_estimator_instance):
    """Test BaseEstimator `is_fitted` property returns expected value."""
    expected_value_unfitted = (
        fixture_estimator_instance.is_fitted == fixture_estimator_instance._is_fitted
    )
    fixture_estimator_instance.fit()
    expected_value_fitted = (
        fixture_estimator_instance.is_fitted == fixture_estimator_instance._is_fitted
    )
    assert (
        expected_value_unfitted and expected_value_fitted
    ), "`BaseEstimator` property `is_fitted` does not return `_is_fitted` value."


def test_check_is_fitted_raises_error_on_unfitted_estimator(fixture_estimator_instance):
    """Test BaseEstimator `check_is_fitted` method raises an error."""
    name = fixture_estimator_instance.__class__.__name__
    match = f"This instance of {name} has not been fitted yet; please call `fit` first."
    with pytest.raises(NotFittedError, match=match):
        fixture_estimator_instance.check_is_fitted()
