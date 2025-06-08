# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for BaseMetaObject and BaseMetaEstimator mixins."""

__author__ = ["RNKuhns", "fkiraly"]
import inspect

import pytest

from skbase._exceptions import NotFittedError
from skbase.base import BaseEstimator, BaseObject
from skbase.base._meta import (
    BaseMetaEstimator,
    BaseMetaObject,
    _MetaObjectMixin,
    _MetaTagLogicMixin,
)


class MetaObjectTester(BaseMetaObject):
    """Class to test meta-object functionality."""

    def __init__(self, a=7, b="something", c=None, steps=None):
        self.a = a
        self.b = b
        self.c = c
        self.steps = steps
        super().__init__()


class MetaEstimatorTester(BaseMetaEstimator):
    """Class to test meta-estimator functionality."""

    def __init__(self, a=7, b="something", c=None, steps=None):
        self.a = a
        self.b = b
        self.c = c
        self.steps = steps
        super().__init__()


class ComponentDummy(BaseObject):
    """Class to use as components in meta-estimator."""

    def __init__(self, a=7, b="something"):
        self.a = a
        self.b = b
        super().__init__()


@pytest.fixture
def fixture_metaestimator_instance():
    """BaseMetaEstimator instance fixture."""
    return BaseMetaEstimator()


@pytest.fixture
def fixture_meta_object():
    """MetaObjectTester instance fixture."""
    return MetaObjectTester()


@pytest.fixture
def fixture_meta_estimator():
    """MetaEstimatorTester instance fixture."""
    return MetaEstimatorTester()


def test_is_composite_returns_true(fixture_meta_object, fixture_meta_estimator):
    """Test that `is_composite` method returns True."""
    msg = "`is_composite` should always be True for subclasses of "
    assert fixture_meta_object.is_composite() is True, msg + "`BaseMetaObject`."
    assert fixture_meta_estimator.is_composite() is True, msg + "`BaseMetaEstimator`."


def test_basemetaestimator_inheritance(fixture_metaestimator_instance):
    """Check BaseMetaEstimator correctly inherits from BaseEstimator and BaseObject."""
    estimator_is_subclass_of_baseobejct = issubclass(BaseMetaEstimator, BaseObject)
    estimator_instance_is_baseobject_instance = isinstance(
        fixture_metaestimator_instance, BaseObject
    )

    # Verify that BaseMetaEstimator is an estimator
    assert (
        estimator_is_subclass_of_baseobejct
        and estimator_instance_is_baseobject_instance
    ), "`BaseMetaEstimator` not correctly subclassing `BaseEstimator` and `BaseObject`."

    # Verify expected MRO inherittence order
    assert BaseMetaEstimator.__mro__[:-2] == (
        BaseMetaEstimator,
        _MetaObjectMixin,
        _MetaTagLogicMixin,
        BaseEstimator,
        BaseObject,
    ), "`BaseMetaEstimator` has incorrect mro."


def test_basemetaestimator_has_is_fitted(fixture_metaestimator_instance):
    """Test BaseEstimator has `is_fitted` property."""
    has_private_is_fitted = hasattr(fixture_metaestimator_instance, "_is_fitted")
    has_is_fitted = hasattr(fixture_metaestimator_instance, "is_fitted")
    assert (
        has_private_is_fitted and has_is_fitted
    ), "`BaseMetaEstimator` does not have `is_fitted` property or `_is_fitted` attr."


def test_basemetaestimator_has_check_is_fitted(fixture_metaestimator_instance):
    """Test BaseEstimator has `check_is_fitted` method."""
    has_check_is_fitted = hasattr(fixture_metaestimator_instance, "check_is_fitted")
    is_method = inspect.ismethod(fixture_metaestimator_instance.check_is_fitted)
    assert (
        has_check_is_fitted and is_method
    ), "`BaseMetaEstimator` does not have `check_is_fitted` method."


@pytest.mark.parametrize("is_fitted_value", (True, False))
def test_basemetaestimator_is_fitted(fixture_metaestimator_instance, is_fitted_value):
    """Test BaseEstimator `is_fitted` property returns expected value."""
    fixture_metaestimator_instance._is_fitted = is_fitted_value
    expected_value_unfitted = (
        fixture_metaestimator_instance.is_fitted
        == fixture_metaestimator_instance._is_fitted
    )
    assert (
        expected_value_unfitted
    ), "`BaseMetaEstimator` property `is_fitted` does not return `_is_fitted` value."


def test_basemetaestimator_check_is_fitted_raises_error_when_unfitted(
    fixture_metaestimator_instance,
):
    """Test BaseEstimator `check_is_fitted` method raises an error."""
    name = fixture_metaestimator_instance.__class__.__name__
    match = f"This instance of {name} has not been fitted yet. Please call `fit` first."
    with pytest.raises(NotFittedError, match=match):
        fixture_metaestimator_instance.check_is_fitted()

    fixture_metaestimator_instance._is_fitted = True
    assert fixture_metaestimator_instance.check_is_fitted() is None


@pytest.mark.parametrize("long_steps", (True, False))
def test_metaestimator_composite(long_steps):
    """Test composite meta-estimator functionality."""
    if long_steps:
        steps = [("foo", ComponentDummy(42)), ("bar", ComponentDummy(24))]
    else:
        steps = [("foo", ComponentDummy(42), 123), ("bar", ComponentDummy(24), 321)]

    meta_est = MetaEstimatorTester(steps=steps)

    meta_est_params = meta_est.get_params()
    assert isinstance(meta_est_params, dict)
    expected_keys = [
        "a",
        "b",
        "c",
        "steps",
        "foo",
        "bar",
        "foo__a",
        "foo__b",
        "bar__a",
        "bar__b",
    ]
    assert set(meta_est_params.keys()) == set(expected_keys)

    meta_est.set_params(bar__b="something else")
    assert meta_est.get_params()["bar__b"] == "something else"


def test_meta_object_reset_consistency():
    """Test that BaseMetaObject resets
    consistently with BaseObject during set_params."""
    # Test that BaseMetaObject resets on set_params call like BaseObject
    meta_obj = MetaObjectTester(a=1, b="test", steps=[])

    # Add attributes that should be removed by reset
    meta_obj.some_attribute = "test"
    meta_obj.fitted_attribute_ = "fitted"

    assert hasattr(meta_obj, "some_attribute")
    assert hasattr(meta_obj, "fitted_attribute_")

    # Set parameters - this should trigger reset
    meta_obj.set_params(a=3)

    # Check that reset occurred
    assert not hasattr(meta_obj, "some_attribute")
    assert not hasattr(meta_obj, "fitted_attribute_")
    assert meta_obj.a == 3


def test_meta_object_reset_with_steps():
    """Test that BaseMetaObject resets correctly
    when setting steps and step parameters."""
    step1 = ComponentDummy(a=100, b="step1")
    step2 = ComponentDummy(a=300, b="step2")

    meta_obj = MetaObjectTester(
        a=1, b="main", steps=[("old_step", ComponentDummy(a=999, b="old"))]
    )

    # Add attributes that should be removed by reset
    meta_obj.some_attribute = "test"
    meta_obj.fitted_attribute_ = "fitted"

    assert hasattr(meta_obj, "some_attribute")
    assert hasattr(meta_obj, "fitted_attribute_")

    # Set both steps parameter and step-specific parameters
    new_steps = [("step1", step1), ("step2", step2)]
    meta_obj.set_params(steps=new_steps, step1__a=500)

    # Check that reset occurred
    assert not hasattr(meta_obj, "some_attribute")
    assert not hasattr(meta_obj, "fitted_attribute_")

    # Check that parameters were set correctly
    assert meta_obj.a == 1  # Should remain unchanged
    assert len(meta_obj.steps) == 2
    assert meta_obj.steps[0][0] == "step1"
    assert meta_obj.steps[0][1].a == 500  # Should be modified by step1__a parameter
    assert meta_obj.steps[1][0] == "step2"
    assert meta_obj.steps[1][1].a == 300  # Should remain unchanged


def test_meta_estimator_reset_consistency():
    """Test that BaseMetaEstimator resets
    consistently with BaseObject during set_params."""
    # Test that BaseMetaEstimator resets on set_params call like BaseObject
    meta_est = MetaEstimatorTester(a=1, b="test", steps=[])

    # Add attributes that should be removed by reset
    meta_est.some_attribute = "test"
    meta_est.fitted_attribute_ = "fitted"

    assert hasattr(meta_est, "some_attribute")
    assert hasattr(meta_est, "fitted_attribute_")

    # Set parameters - this should trigger reset
    meta_est.set_params(a=3)

    # Check that reset occurred
    assert not hasattr(meta_est, "some_attribute")
    assert not hasattr(meta_est, "fitted_attribute_")
    assert meta_est.a == 3
