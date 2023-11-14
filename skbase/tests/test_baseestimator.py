# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for BaseEstimator class.

tests in this module:

    test_baseestimator_inheritance - Test BaseEstimator inherits from BaseObject.
    test_has_is_fitted - Test that BaseEstimator has is_fitted interface.
    test_has_check_is_fitted - Test that BaseEstimator has check_is_fitted interface.
    test_is_fitted  - Test that is_fitted property returns _is_fitted as expected.
    test_check_is_fitted_raises_error_when_unfitted - Test check_is_fitted raises error.
"""

__author__ = ["fkiraly", "RNKuhns"]
import inspect
from copy import deepcopy

import pytest

from skbase._exceptions import NotFittedError
from skbase.base import BaseEstimator, BaseObject


@pytest.fixture
def fixture_estimator():
    """Pytest fixture of BaseEstimator class."""
    return BaseEstimator


@pytest.fixture
def fixture_estimator_instance():
    """Pytest fixture of BaseEstimator instance."""
    return BaseEstimator()


def test_baseestimator_inheritance(fixture_estimator, fixture_estimator_instance):
    """Check BaseEstimator correctly inherits from BaseObject."""
    estimator_is_subclass_of_baseobejct = issubclass(fixture_estimator, BaseObject)
    estimator_instance_is_baseobject_instance = isinstance(
        fixture_estimator_instance, BaseObject
    )
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
    assert (
        expected_value_unfitted
    ), "`BaseEstimator` property `is_fitted` does not return `_is_fitted` value."


def test_check_is_fitted_raises_error_when_unfitted(fixture_estimator_instance):
    """Test BaseEstimator `check_is_fitted` method raises an error."""
    name = fixture_estimator_instance.__class__.__name__
    match = f"This instance of {name} has not been fitted yet. Please call `fit` first."
    with pytest.raises(NotFittedError, match=match):
        fixture_estimator_instance.check_is_fitted()

    fixture_estimator_instance._is_fitted = True
    assert fixture_estimator_instance.check_is_fitted() is None


class FittableCompositionDummy(BaseEstimator):
    """Potentially composite object, for testing."""

    def __init__(self, foo, bar=84):
        self.foo = foo
        self.foo_ = deepcopy(foo)
        self.bar = bar

    def fit(self):
        """Fit, dummy."""
        if hasattr(self.foo_, "fit"):
            self.foo_.fit()
        self._is_fitted = True


def test_get_fitted_params():
    """Tests fitted parameter retrieval.

    Raises
    ------
    AssertionError if logic behind get_fitted_params is incorrect, logic tested:
        calling get_fitted_params on a non-composite fittable returns the fitted param
        calling get_fitted_params on a composite returns all nested params
    """
    non_composite = FittableCompositionDummy(foo=42)
    composite = FittableCompositionDummy(foo=deepcopy(non_composite))

    non_composite.fit()
    composite.fit()

    non_comp_f_params = non_composite.get_fitted_params()
    comp_f_params = composite.get_fitted_params()
    comp_f_params_shallow = composite.get_fitted_params(deep=False)

    assert isinstance(non_comp_f_params, dict)
    assert set(non_comp_f_params.keys()) == {"foo"}

    assert isinstance(comp_f_params, dict)
    assert set(comp_f_params) == {"foo", "foo__foo"}
    assert set(comp_f_params_shallow) == {"foo"}
    assert comp_f_params["foo"] is composite.foo_
    assert comp_f_params["foo"] is not composite.foo
    assert comp_f_params_shallow["foo"] is composite.foo_
    assert comp_f_params_shallow["foo"] is not composite.foo
