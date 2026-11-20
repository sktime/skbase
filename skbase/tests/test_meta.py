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
from skbase.base._tagmanager import _FlagManager


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

    # Verify expected MRO inheritance order
    mro_filtered = tuple(c for c in BaseMetaEstimator.__mro__ if c is not object)
    assert mro_filtered == (
        BaseMetaEstimator,
        _MetaObjectMixin,
        _MetaTagLogicMixin,
        BaseEstimator,
        BaseObject,
        _FlagManager,
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


def test_check_objects_attr_name_auto_detection():
    """Test that _check_objects auto-detects attr_name from tag."""

    steps = [ComponentDummy(42), ComponentDummy(24)]
    meta_obj = MetaObjectTester(steps=steps)

    # auto-detect from tag
    result = meta_obj._check_objects(steps, attr_name=None)

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    assert all(isinstance(item[0], str) for item in result)
    assert all(isinstance(item[1], ComponentDummy) for item in result)

    with pytest.raises(TypeError, match="'steps'"):
        meta_obj._check_objects(None, attr_name=None)


def test_check_objects_attr_name_explicit():
    """Test that _check_objects works with explicit attr_name."""
    # Create a meta object with steps
    steps = [ComponentDummy(42), ComponentDummy(24)]
    meta_obj = MetaObjectTester(steps=steps)

    # Test with explicit attr_name
    result = meta_obj._check_objects(steps, attr_name="custom_steps")

    assert isinstance(result, list)
    assert len(result) == 2

    with pytest.raises(TypeError, match="'custom_steps'"):
        meta_obj._check_objects(None, attr_name="custom_steps")


def test_check_objects_attr_name_custom_tag():
    """Test that _check_objects auto-detects from custom named_object_parameters tag."""
    # custom tag
    meta_obj = MetaObjectTester()
    meta_obj.set_tags(**{"named_object_parameters": "components"})

    components = [ComponentDummy(1), ComponentDummy(2)]

    # should auto-detect custom tag
    result = meta_obj._check_objects(components, attr_name=None)

    assert isinstance(result, list)
    assert len(result) == 2

    with pytest.raises(TypeError, match="'components'"):
        meta_obj._check_objects(None, attr_name=None)


def test_set_params_resets_fitted_state():
    """Test that set_params calls reset, removing fitted state.

    Regression test for issue #412.
    BaseMetaObject should call reset() during set_params() to clear fitted state,
    maintaining consistency with BaseObject behavior.
    """
    steps = [("foo", ComponentDummy(42)), ("bar", ComponentDummy(24))]
    meta_obj = MetaObjectTester(steps=steps)

    # Add some fitted state (simulating a fit operation)
    meta_obj.fitted_attr_ = "should be removed after set_params"
    meta_obj.another_fitted_ = 123

    # Test 1: Setting the named object parameter should trigger reset
    new_steps = [("foo", ComponentDummy(99))]
    meta_obj.set_params(steps=new_steps)

    # Fitted state should be gone after set_params
    assert not hasattr(
        meta_obj, "fitted_attr_"
    ), "fitted_attr_ should be removed by reset() during set_params(steps=...)"
    assert not hasattr(
        meta_obj, "another_fitted_"
    ), "another_fitted_ should be removed by reset() during set_params(steps=...)"

    # Test 2: Replacing individual step should also trigger reset
    meta_obj = MetaObjectTester(steps=steps)
    meta_obj.fitted_attr_ = "should be removed"

    meta_obj.set_params(foo=ComponentDummy(77))

    assert not hasattr(
        meta_obj, "fitted_attr_"
    ), "fitted_attr_ should be removed by reset() during set_params(foo=...)"


def test_get_class_flags_preserves_mixin_tags():
    """Regression test for Issue #539.

    `_get_class_flags` previously sliced the MRO with ``[:-2]``, assuming the
    last two entries are always ``BaseObject`` and ``object``.  Under multiple
    inheritance Python's C3 linearisation can place a user-defined Mixin class
    *after* ``BaseObject`` (i.e. at position -2), so the slice permanently
    dropped any flags defined on that Mixin.

    The fix iterates the full MRO and skips only ``object`` explicitly so that
    every user-defined class – regardless of its MRO position – contributes its
    flags.  This test pins that behaviour to prevent regressions.
    """

    class MyMixin:
        """Mixin that defines a tag.  Has no _FlagManager inheritance."""

        _flags = {"mixin_tag": 42}

    # Inheriting BaseObject *before* MyMixin forces MyMixin to the tail of the
    # MRO (just before `object`), which is exactly the scenario that was broken.
    class MyObj(BaseObject, MyMixin):
        """Concrete class using multiple inheritance."""

        _flags = {"own_tag": 1}

        def __init__(self):
            super().__init__()

    mro_classes = [c.__name__ for c in MyObj.__mro__]

    # Sanity-check: MyMixin should be near the tail (after BaseObject).
    assert mro_classes.index("MyMixin") > mro_classes.index(
        "BaseObject"
    ), "Test setup error: MyMixin should appear after BaseObject in the MRO."

    collected = MyObj._get_class_flags()

    # Both own_tag and mixin_tag must be present.
    assert (
        "own_tag" in collected
    ), "'own_tag' defined directly on MyObj was not collected."
    assert "mixin_tag" in collected, (
        "Regression (Issue #539): 'mixin_tag' from MyMixin was dropped by "
        "_get_class_flags.  The MRO slice [:-2] is being used again – revert "
        "to the explicit `if parent_class is object: continue` check."
    )
    assert collected["mixin_tag"] == 42
    assert collected["own_tag"] == 1


def test_check_objects_attr_name_none_tag_not_set():
    """Test error when attr_name is None and tag is not set or returns None."""
    meta_obj = MetaObjectTester()

    # Set tag to None explicitly
    meta_obj.set_tags(**{"named_object_parameters": None})

    steps = [ComponentDummy(1)]

    with pytest.raises(TypeError, match="could not be auto-detected.*non-empty string"):
        meta_obj._check_objects(steps, attr_name=None)


# Tests for _MetaObjectMixin error paths and helper methods
# ---------------------------------------------------------


def test_check_names_valid():
    """Test _check_names returns valid names unchanged."""
    meta_obj = MetaObjectTester()
    names = ["comp1", "comp2"]

    assert meta_obj._check_names(names, make_unique=True) == ["comp1", "comp2"]
    assert meta_obj._check_names(names, make_unique=False) == ["comp1", "comp2"]


def test_check_names_duplicate_raises():
    """Test _check_names raises ValueError when names are not unique."""
    meta_obj = MetaObjectTester()

    with pytest.raises(ValueError, match="Names provided are not unique"):
        meta_obj._check_names(["comp1", "comp1"])


@pytest.mark.parametrize(
    "invalid_names",
    [
        ["a", "comp1"],
        ["steps", "comp1"],
        ["comp__1", "comp2"],
        ["a", "bad__name"],
    ],
)
def test_check_names_conflict_or_dunder_raises(invalid_names):
    """Test _check_names raises ValueError on param conflict or '__' in name."""
    meta_obj = MetaObjectTester()

    with pytest.raises(
        ValueError, match="conflict with constructor argument or contain '__'"
    ):
        meta_obj._check_names(invalid_names)


@pytest.mark.parametrize(
    "bad_cls_type",
    [
        "BaseObject",
        123,
        (ComponentDummy, "not_a_class"),
    ],
)
def test_validate_objects_invalid_cls_type_raises(bad_cls_type):
    """Test _validate_objects raises TypeError for invalid cls_type."""
    meta_obj = MetaObjectTester()
    steps = [ComponentDummy(1)]

    with pytest.raises(TypeError, match="`cls_type` must be a class or tuple of"):
        meta_obj._validate_objects(steps, attr_name="steps", cls_type=bad_cls_type)


def test_validate_objects_cls_type_class_and_tuple():
    """Test _validate_objects with single class and tuple of classes for cls_type."""
    meta_obj = MetaObjectTester()
    comp = ComponentDummy(1)
    est = BaseEstimator()

    # Single class passes for matching instance, fails for non-matching
    assert meta_obj._validate_objects(
        [comp], attr_name="steps", cls_type=ComponentDummy
    )
    with pytest.raises(TypeError, match="must be of type ComponentDummy"):
        meta_obj._validate_objects([est], attr_name="steps", cls_type=ComponentDummy)

    # Tuple of classes passes for both, fails for non-matching
    cls_tuple = (ComponentDummy, BaseEstimator)
    assert meta_obj._validate_objects(
        [comp, est], attr_name="steps", cls_type=cls_tuple
    )
    with pytest.raises(
        TypeError, match="must be of type ComponentDummy or BaseEstimator"
    ):
        meta_obj._validate_objects(
            [BaseObject()], attr_name="steps", cls_type=cls_tuple
        )


def test_validate_objects_invalid_dict_and_list_elements():
    """Test _validate_objects raises TypeError for invalid dict or list elements."""
    meta_obj = MetaObjectTester()

    # Invalid dict: non-str key or wrong value type
    with pytest.raises(TypeError, match="Invalid 'steps' attribute"):
        meta_obj._validate_objects(
            {1: ComponentDummy()}, attr_name="steps", allow_dict=True
        )
    with pytest.raises(TypeError, match="Invalid 'steps' attribute"):
        meta_obj._validate_objects(
            {"c1": "not_an_object"}, attr_name="steps", allow_dict=True
        )

    # Invalid list element
    with pytest.raises(TypeError, match="Invalid 'steps' attribute"):
        meta_obj._validate_objects(["not_an_object"], attr_name="steps")


def test_validate_objects_mixed_not_allowed():
    """Test _validate_objects raises TypeError when mix is disallowed."""
    meta_obj = MetaObjectTester()
    mixed = [ComponentDummy(1), ("c2", ComponentDummy(2))]

    with pytest.raises(TypeError, match="A mix of the two is not allowed"):
        meta_obj._validate_objects(mixed, attr_name="steps", allow_mix=False)


def test_coerce_object_tuple_and_dict_helpers():
    """Test _coerce_object_tuple 1-tuple and dict handling in name/object helpers."""
    meta_obj = MetaObjectTester()
    comp1 = ComponentDummy(1)
    comp2 = ComponentDummy(2)

    assert meta_obj._coerce_object_tuple((comp1,)) == ("ComponentDummy", comp1)

    obj_dict = {"first": comp1, "second": comp2}
    names, objs = meta_obj._get_names_and_objects(obj_dict)
    assert names == ["first", "second"]
    assert objs == [comp1, comp2]

    coerced = meta_obj._coerce_to_named_object_tuples(obj_dict)
    assert coerced == [("first", comp1), ("second", comp2)]


def test_set_params_empty_returns_self():
    """Test set_params with no keyword arguments returns self."""
    meta_obj = MetaObjectTester(steps=[ComponentDummy(1)])
    assert meta_obj.set_params() is meta_obj


@pytest.mark.parametrize(
    "kwargs, exc_type, match",
    [
        (
            {
                "base_class": BaseObject,
                "composite_class": MetaObjectTester,
                "concat_order": "middle",
            },
            ValueError,
            "`concat_order` must be 'left' or 'right'",
        ),
        (
            {
                "base_class": BaseObject,
                "composite_class": MetaObjectTester,
                "attr_name": 123,
            },
            TypeError,
            "`attr_name` must be str",
        ),
        (
            {
                "base_class": BaseObject,
                "composite_class": "not_a_class",
            },
            TypeError,
            "`composite_class` must be a class",
        ),
        (
            {
                "base_class": "not_a_class",
                "composite_class": MetaObjectTester,
            },
            TypeError,
            "`base_class` must be a class",
        ),
        (
            {
                "base_class": ComponentDummy,
                "composite_class": MetaObjectTester,
            },
            ValueError,
            "`composite_class` must be a subclass of base_class",
        ),
        (
            {
                "base_class": BaseObject,
                "composite_class": MetaEstimatorTester,
            },
            TypeError,
            "self must be an instance of `composite_class`",
        ),
    ],
)
def test_dunder_concat_validation_errors(kwargs, exc_type, match):
    """Test _dunder_concat raises expected errors on invalid arguments."""
    meta_obj = MetaObjectTester(steps=[ComponentDummy(1)])
    other = ComponentDummy(2)

    with pytest.raises(exc_type, match=match):
        meta_obj._dunder_concat(other=other, **kwargs)


def test_dunder_concat_composites_and_base_objects():
    """Test _dunder_concat with composites, base objects, named tuples, and params."""
    c1 = ComponentDummy(1)
    c2 = ComponentDummy(2)
    c3 = ComponentDummy(3)

    m1 = MetaObjectTester(steps=[c1])
    m2 = MetaObjectTester(steps=[c2])

    # Left and right concatenation of two composites (all default class names -> list)
    left = m1._dunder_concat(m2, BaseObject, MetaObjectTester, concat_order="left")
    assert isinstance(left, MetaObjectTester)
    assert left.steps == [c1, c2]

    right = m1._dunder_concat(m2, BaseObject, MetaObjectTester, concat_order="right")
    assert right.steps == [c2, c1]

    # Concatenation with a single base_class instance
    with_base = m1._dunder_concat(c3, BaseObject, MetaObjectTester)
    assert with_base.steps == [c1, c3]

    # Concatenation with a named (str, base_class) tuple keeps named tuples
    with_named = m1._dunder_concat(("custom", c3), BaseObject, MetaObjectTester)
    assert with_named.steps == [("ComponentDummy", c1), ("custom", c3)]

    # composite_params are forwarded without mutating the input dict
    extra_params = {"a": 99, "b": "extra"}
    with_params = m1._dunder_concat(
        c2, BaseObject, MetaObjectTester, composite_params=extra_params
    )
    assert with_params.a == 99
    assert with_params.b == "extra"
    assert "steps" not in extra_params

    # Incompatible other returns NotImplemented
    assert m1._dunder_concat("not_an_object", BaseObject, MetaObjectTester) is (
        NotImplemented
    )


def test_metaestimator_get_fitted_params():
    """Test _get_fitted_params / get_fitted_params on a fitted BaseMetaEstimator."""

    class FittedComponent(BaseEstimator):
        def __init__(self, x=1):
            self.x = x
            super().__init__()

        def fit(self):
            self.learned_ = self.x * 10
            self._is_fitted = True
            return self

    class FittedMetaEstimator(BaseMetaEstimator):
        _tags = {
            "named_object_parameters": "steps",
            "fitted_named_object_parameters": "steps_",
        }

        def __init__(self, steps=None):
            self.steps = steps
            super().__init__()

        def fit(self):
            self.steps_ = [(name, est.clone().fit()) for name, est in self.steps]
            self.meta_param_ = "fitted"
            self._is_fitted = True
            return self

    meta_est = FittedMetaEstimator(
        steps=[("c1", FittedComponent(2)), ("c2", FittedComponent(3))]
    ).fit()

    fitted = meta_est.get_fitted_params()
    assert fitted["meta_param"] == "fitted"
    assert fitted["c1__learned"] == 20
    assert fitted["c2__learned"] == 30
