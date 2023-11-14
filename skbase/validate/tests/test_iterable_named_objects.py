# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests of the functionality for validating iterables of named objects.

tests in this module include:

- test_is_named_object_tuple_output
- test_is_sequence_named_objects_output
- test_check_sequence_named_objects_output
"""

__author__ = ["RNKuhns"]
import pytest

from skbase.base import BaseEstimator, BaseObject
from skbase.validate import (
    check_sequence_named_objects,
    is_named_object_tuple,
    is_sequence_named_objects,
)


@pytest.fixture
def fixture_object_instance():
    """Pytest fixture of BaseObject instance."""
    return BaseObject()


@pytest.fixture
def fixture_estimator_instance():
    """Pytest fixture of BaseEstimator instance."""
    return BaseEstimator()


def test_is_named_object_tuple_output(
    fixture_estimator_instance, fixture_object_instance
):
    """Test is_named_object_tuple returns expected value."""
    # Default checks for object to be an instance of BaseObject
    assert is_named_object_tuple(("Step 1", fixture_object_instance)) is True
    assert is_named_object_tuple(("Step 2", fixture_estimator_instance)) is True

    # If a different `object_type` is provided then it is used in the isinstance check

    assert (
        is_named_object_tuple(
            ("Step 1", fixture_object_instance), object_type=BaseEstimator
        )
        is False
    )
    assert (
        is_named_object_tuple(
            ("Step 1", fixture_estimator_instance), object_type=BaseEstimator
        )
        is True
    )

    # If the input is does not follow named object tuple format then False is returned
    # This checks for named object tuples, so dictionary input is not allowed
    assert is_named_object_tuple({"Step 1": fixture_estimator_instance}) is False
    # First element of tuple must be string
    assert is_named_object_tuple((1, fixture_object_instance)) is False


def test_is_sequence_named_objects_output(
    fixture_estimator_instance, fixture_object_instance
):
    """Test is_sequence_named_objects returns expected value."""
    # Correctly formatted iterables of (name, BaseObject instance) tuples
    named_objects = [
        ("Step 1", fixture_estimator_instance),
        ("Step 2", fixture_object_instance),
    ]
    assert is_sequence_named_objects(named_objects) is True
    assert is_sequence_named_objects(tuple(named_objects)) is True

    # Test correct format, but duplicate names
    named_objects = [
        ("Step 1", fixture_estimator_instance),
        ("Step 1", fixture_object_instance),
    ]
    assert is_sequence_named_objects(named_objects) is True
    assert is_sequence_named_objects(tuple(named_objects)) is True
    # Tests with correctly formatted dictionary
    dict_named_objects = {
        "Step 1": fixture_estimator_instance,
        "Step 2": fixture_object_instance,
    }
    assert is_sequence_named_objects(dict_named_objects) is True
    assert is_sequence_named_objects(dict_named_objects, allow_dict=False) is False

    # Invalid format due to object names not being strings
    incorrectly_named_objects = [
        (1, fixture_estimator_instance),
        (2, fixture_object_instance),
    ]
    assert is_sequence_named_objects(incorrectly_named_objects) is False

    # Invalid format due to named items not being BaseObject instances
    named_items = [("1", 7), ("2", 42)]
    assert is_sequence_named_objects(named_items) is False
    dict_named_objects = {"Step 1": 7, "Step 2": 42}
    assert is_sequence_named_objects(dict_named_objects) is False

    # Invalid because input is not a sequence
    non_sequence = 7
    assert is_sequence_named_objects(non_sequence) is False

    # Generators are also invalid since they don't have length or ability
    # to access individual elements, we don't includein the named object API
    named_objects = [
        ("Step 1", fixture_estimator_instance),
        ("Step 2", fixture_object_instance),
    ]
    assert is_sequence_named_objects(c for c in named_objects) is False

    # Validate use of object_type parameter
    # Won't work because one named object is a BaseObject but not a BaseEstimator
    assert is_sequence_named_objects(named_objects, object_type=BaseEstimator) is False

    # Should work because we allow BaseObject or BaseEstimator types
    named_objects = [("Step 1", BaseEstimator()), ("Step 2", BaseEstimator())]
    assert (
        is_sequence_named_objects(
            named_objects, object_type=(BaseObject, BaseEstimator)
        )
        is True
    )
    assert is_sequence_named_objects(named_objects, object_type=BaseEstimator) is True


def test_check_sequence_named_objects_output(
    fixture_estimator_instance, fixture_object_instance
):
    """Test check_sequence_named_objects returns expected value."""
    # Correctly formatted iterables of (name, BaseObject instance) tuples
    named_objects = [
        ("Step 1", fixture_estimator_instance),
        ("Step 2", fixture_object_instance),
    ]
    assert check_sequence_named_objects(named_objects) == named_objects
    assert check_sequence_named_objects(tuple(named_objects)) == tuple(named_objects)

    # Tests with correctly formatted dictionary
    dict_named_objects = {
        "Step 1": fixture_estimator_instance,
        "Step 2": fixture_object_instance,
    }
    assert check_sequence_named_objects(dict_named_objects) == dict_named_objects
    # Raises an error if we don't allow dicts as part of named object API
    with pytest.raises(ValueError):
        check_sequence_named_objects(dict_named_objects, allow_dict=False)

    # Invalid format due to object names not being strings
    incorrectly_named_objects = [
        (1, fixture_estimator_instance),
        (2, fixture_object_instance),
    ]
    with pytest.raises(ValueError):
        check_sequence_named_objects(incorrectly_named_objects)

    # Invalid format due to named items not being BaseObject instances
    named_items = [("1", 7), ("2", 42)]
    with pytest.raises(ValueError):
        check_sequence_named_objects(named_items)
    dict_named_objects = {"Step 1": 7, "Step 2": 42}
    with pytest.raises(ValueError):
        check_sequence_named_objects(dict_named_objects)

    # Invalid due to not being sequences
    non_sequence = 7
    with pytest.raises(ValueError):
        check_sequence_named_objects(non_sequence)

    # Generators are also invalid since they don't have length or ability
    # to access individual elements, we don't includein the named object API
    named_objects = [
        ("Step 1", fixture_estimator_instance),
        ("Step 2", fixture_object_instance),
    ]
    with pytest.raises(ValueError):
        check_sequence_named_objects(c for c in named_objects)

    # Validate use of object_type parameter
    # Won't work because one named object is a BaseObject but not a BaseEstimator
    with pytest.raises(ValueError):
        check_sequence_named_objects(named_objects, object_type=BaseEstimator)

    # Should work because we allow BaseObject or BaseEstimator types
    named_objects = [("Step 1", BaseEstimator()), ("Step 2", BaseEstimator())]
    assert (
        check_sequence_named_objects(
            named_objects, object_type=(BaseObject, BaseEstimator)
        )
        == named_objects
    )
    assert (
        check_sequence_named_objects(named_objects, object_type=BaseEstimator)
        == named_objects
    )
