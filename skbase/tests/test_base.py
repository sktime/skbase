# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Elements of these tests re-use code developed in scikit-learn. These elements
# are copyrighted by the scikit-learn developers, BSD-3-Clause License. For
# conditions see https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
"""Tests for BaseObject universal base class.

tests in this module:

    test_get_class_tags  - tests get_class_tags inheritance logic
    test_get_class_tag   - tests get_class_tag logic, incl default value
    test_get_tags        - tests get_tags inheritance logic
    test_get_tag         - tests get_tag logic, incl default value
    test_set_tags        - tests set_tags logic and related get_tags inheritance

    test_reset           - tests reset logic on a simple, non-composite estimator
    test_reset_composite - tests reset logic on a composite estimator
    test_components      - tests logic for returning components of composite estimator

    test_get_init_signature
    test_get_init_signature_raises_error_for_invalid_signature
"""

__author__ = ["fkiraly"]

__all__ = [
    "test_get_class_tags",
    "test_get_class_tag",
    "test_get_tags",
    "test_get_tag",
    "test_set_tags",
    "test_reset",
    "test_reset_composite",
]
import inspect
from copy import deepcopy

import pytest
from sklearn import config_context

# TODO: Update with import of skbase clone function once implemented
from sklearn.base import clone

from skbase import BaseObject


# Fixture class for testing tag system
class FixtureClassParent(BaseObject):

    _tags = {"A": "1", "B": 2, "C": 1234, 3: "D"}


# Fixture class for testing tag system, child overrides tags
class FixtureClassChild(FixtureClassParent):

    _tags = {"A": 42, 3: "E"}


FIXTURE_CLASSCHILD = FixtureClassChild
FIXTURE_CLASSCHILD_TAGS = {"A": 42, "B": 2, "C": 1234, 3: "E"}

# Fixture class for testing tag system, object overrides class tags
FIXTURE_OBJECT = FixtureClassChild()
FIXTURE_OBJECT._tags_dynamic = {"A": 42424241, "B": 3}

FIXTURE_OBJECT_TAGS = {"A": 42424241, "B": 3, "C": 1234, 3: "E"}


class InvalidInitSignatureTester(BaseObject):
    def __init__(self, a, *args):
        pass


class Example(BaseObject):
    """Example that illustrates BaseObject usage."""

    def __init__(self, a="something", b=7, c=None):
        self.a = a
        self.b = b
        self.c = c


class Buggy(BaseObject):
    """A buggy BaseObject that does not set its parameters right."""

    def __init__(self, a=None):
        self.a = 1
        self._a = a


class ModifyParam(BaseObject):
    """A non-conforming BaseObject that modifyies parameters in init."""

    def __init__(self, a=None):
        self.a = deepcopy(a)


FIXTURE_INVALID_INIT = InvalidInitSignatureTester
FIXTURE_EXAMPLE = Example
FIXTURE_EXAMPLE_EXPECTED_PARAM_NAMES = ["a", "b", "c"]
FIXTURE_BUGGY = Buggy
FIXTURE_MODIFY_PARAM = ModifyParam


def test_get_class_tags():
    """Test get_class_tags class method of BaseObject for correctness.

    Raises
    ------
    AssertError if inheritance logic in get_class_tags is incorrect
    """
    child_tags = FIXTURE_CLASSCHILD.get_class_tags()

    msg = "Inheritance logic in BaseObject.get_class_tags is incorrect"

    assert child_tags == FIXTURE_CLASSCHILD_TAGS, msg


def test_get_class_tag():
    """Test get_class_tag class method of BaseObject for correctness.

    Raises
    ------
    AssertError if inheritance logic in get_tag is incorrect
    AssertError if default override logic in get_tag is incorrect
    """
    child_tags = {}
    child_tags_keys = FIXTURE_CLASSCHILD_TAGS.keys()

    for key in child_tags_keys:
        child_tags[key] = FIXTURE_CLASSCHILD.get_class_tag(key)

    child_tag_default = FIXTURE_CLASSCHILD.get_class_tag("foo", "bar")
    child_tag_default_none = FIXTURE_CLASSCHILD.get_class_tag("bar")

    msg = "Inheritance logic in BaseObject.get_class_tag is incorrect"

    for key in child_tags_keys:
        assert child_tags[key] == FIXTURE_CLASSCHILD_TAGS[key], msg

    msg = "Default override logic in BaseObject.get_class_tag is incorrect"

    assert child_tag_default == "bar", msg
    assert child_tag_default_none is None, msg


def test_get_tags():
    """Test get_tags method of BaseObject for correctness.

    Raises
    ------
    AssertError if inheritance logic in get_tags is incorrect
    """
    object_tags = FIXTURE_OBJECT.get_tags()

    msg = "Inheritance logic in BaseObject.get_tags is incorrect"

    assert object_tags == FIXTURE_OBJECT_TAGS, msg


def test_get_tag():
    """Test get_tag method of BaseObject for correctness.

    Raises
    ------
    AssertError if inheritance logic in get_tag is incorrect
    AssertError if default override logic in get_tag is incorrect
    """
    object_tags = {}
    object_tags_keys = FIXTURE_OBJECT_TAGS.keys()

    for key in object_tags_keys:
        object_tags[key] = FIXTURE_OBJECT.get_tag(key, raise_error=False)

    object_tag_default = FIXTURE_OBJECT.get_tag("foo", "bar", raise_error=False)
    object_tag_default_none = FIXTURE_OBJECT.get_tag("bar", raise_error=False)

    msg = "Inheritance logic in BaseObject.get_tag is incorrect"

    for key in object_tags_keys:
        assert object_tags[key] == FIXTURE_OBJECT_TAGS[key], msg

    msg = "Default override logic in BaseObject.get_tag is incorrect"

    assert object_tag_default == "bar", msg
    assert object_tag_default_none is None, msg


def test_get_tag_raises():
    """Test that get_tag method raises error for unknown tag.

    Raises
    ------
    AssertError if get_tag does not raise error for unknown tag.
    """
    with pytest.raises(ValueError, match=r"Tag with name"):
        FIXTURE_OBJECT.get_tag("bar")


FIXTURE_TAG_SET = {"A": 42424243, "E": 3}
FIXTURE_OBJECT_SET = deepcopy(FIXTURE_OBJECT).set_tags(**FIXTURE_TAG_SET)
FIXTURE_OBJECT_SET_TAGS = {"A": 42424243, "B": 3, "C": 1234, 3: "E", "E": 3}
FIXTURE_OBJECT_SET_DYN = {"A": 42424243, "B": 3, "E": 3}


def test_set_tags():
    """Test set_tags method of BaseObject for correctness.

    Raises
    ------
    AssertionError if override logic in set_tags is incorrect
    """
    msg = "Setter/override logic in BaseObject.set_tags is incorrect"

    assert FIXTURE_OBJECT_SET._tags_dynamic == FIXTURE_OBJECT_SET_DYN, msg
    assert FIXTURE_OBJECT_SET.get_tags() == FIXTURE_OBJECT_SET_TAGS, msg


class CompositionDummy(BaseObject):
    """Potentially composite object, for testing."""

    def __init__(self, foo, bar=84):
        self.foo = foo
        self.foo_ = deepcopy(foo)
        self.bar = bar


def test_is_composite():
    """Test is_composite tag for correctness.

    Raises
    ------
    AssertionError if logic behind is_composite is incorrect
    """
    non_composite = CompositionDummy(foo=42)
    composite = CompositionDummy(foo=non_composite)

    assert not non_composite.is_composite()
    assert composite.is_composite()


class ResetTester(BaseObject):

    clsvar = 210

    def __init__(self, a, b=42):
        self.a = a
        self.b = b
        self.c = 84

    def foo(self, d=126):
        self.d = deepcopy(d)
        self._d = deepcopy(d)
        self.d_ = deepcopy(d)
        self.f__o__o = 252


def test_reset():
    """Test reset method for correct behaviour, on a simple estimator.

    Raises
    ------
    AssertionError if logic behind reset is incorrect, logic tested:
        reset should remove any object attributes that are not hyper-parameters,
        with the exception of attributes containing double-underscore "__"
        reset should not remove class attributes or methods
        reset should set hyper-parameters as in pre-reset state
    """
    x = ResetTester(168)
    x.foo()

    x.reset()

    assert hasattr(x, "a") and x.a == 168
    assert hasattr(x, "b") and x.b == 42
    assert hasattr(x, "c") and x.c == 84
    assert hasattr(x, "clsvar") and x.clsvar == 210
    assert not hasattr(x, "d")
    assert not hasattr(x, "_d")
    assert not hasattr(x, "d_")
    assert hasattr(x, "f__o__o") and x.f__o__o == 252
    assert hasattr(x, "foo")


def test_reset_composite():
    """Test reset method for correct behaviour, on a composite estimator."""
    y = ResetTester(42)
    x = ResetTester(a=y)

    x.foo(y)
    x.d.foo()

    x.reset()

    assert hasattr(x, "a")
    assert not hasattr(x, "d")
    assert not hasattr(x.a, "d")


def test_components():
    """Test component retrieval.

    Raises
    ------
    AssertionError if logic behind _components is incorrect, logic tested:
        calling _components on a non-composite returns an empty dict
        calling _components on a composite returns name/BaseObject pair in dict,
        and BaseObject returned is identical with attribute of the same name
    """
    non_composite = CompositionDummy(foo=42)
    composite = CompositionDummy(foo=non_composite)

    non_comp_comps = non_composite._components()
    comp_comps = composite._components()

    assert isinstance(non_comp_comps, dict)
    assert set(non_comp_comps.keys()) == set()

    assert isinstance(comp_comps, dict)
    assert set(comp_comps.keys()) == {"foo_"}
    assert comp_comps["foo_"] == composite.foo_
    assert comp_comps["foo_"] != composite.foo


def test_get_init_signature():
    """Test error is raised when invalid init signature is used."""
    init_sig = FIXTURE_EXAMPLE._get_init_signature()
    init_sig_is_list = isinstance(init_sig, list)
    init_sig_elements_are_params = all(
        isinstance(p, inspect.Parameter) for p in init_sig
    )
    assert (
        init_sig_is_list and init_sig_elements_are_params
    ), "`_get_init_signature` is not returning expected result."


def test_get_init_signature_raises_error_for_invalid_signature():
    """Test error is raised when invalid init signature is used."""
    with pytest.raises(RuntimeError):
        FIXTURE_INVALID_INIT._get_init_signature()


def test_get_param_names():
    """Test that get_param_names returns list of string parameter names."""
    param_names = FIXTURE_EXAMPLE.get_param_names()
    assert param_names == sorted(FIXTURE_EXAMPLE_EXPECTED_PARAM_NAMES)

    param_names = BaseObject.get_param_names()
    assert param_names == []


# This section tests the clone functionality
# These have been adapted from sklearn's tests of clone to use the clone
# method that is included as part of the BaseObject interface
def test_clone():
    """Test that clone is making a deep copy as expected."""
    # Creates a BaseObject and makes a copy of its original state
    # (which, in this case, is the current state of the BaseObject),
    # and check that the obtained copy is a correct deep copy.
    base_obj = FIXTURE_EXAMPLE(a=7.0, b="some_str")
    new_base_obj = base_obj.clone()
    assert base_obj is not new_base_obj
    assert base_obj.get_params() == new_base_obj.get_params()


def test_clone_2():
    """Test that clone does not copy attributes not set in constructor."""
    # We first create an estimator, give it an own attribute, and
    # make a copy of its original state. Then we check that the copy doesn't
    # have the specific attribute we manually added to the initial estimator.

    base_obj = FIXTURE_EXAMPLE(a=7.0, b="some_str")
    base_obj.own_attribute = "test"
    new_base_obj = base_obj.clone()
    assert not hasattr(new_base_obj, "own_attribute")


def test_clone_raises_error_for_nonconforming_objects():
    """Test that clone raises an error on nonconforming BaseObjects."""
    buggy = FIXTURE_BUGGY()
    buggy.a = 2
    with pytest.raises(RuntimeError):
        buggy.clone()

    varg_obj = FIXTURE_INVALID_INIT(a=7)
    with pytest.raises(RuntimeError):
        varg_obj.clone()

    obj_that_modifies = FIXTURE_MODIFY_PARAM(a=[0])
    with pytest.raises(RuntimeError):
        obj_that_modifies.clone()


# def test_clone_empty_array():
#     # Regression test for cloning estimators with empty arrays
#     clf = MyEstimator(empty=np.array([]))
#     clf2 = clone(clf)
#     assert_array_equal(clf.empty, clf2.empty)

#     clf = MyEstimator(empty=sp.csr_matrix(np.array([[0]])))
#     clf2 = clone(clf)
#     assert_array_equal(clf.empty.data, clf2.empty.data)


# def test_clone_nan():
#     # Regression test for cloning estimators with default parameter as np.nan
#     clf = MyEstimator(empty=np.nan)
#     clf2 = clone(clf)

#     assert clf.empty is clf2.empty


def test_clone_estimator_types():
    """Test clone works for parameters that are types rather than instances."""
    base_obj = Example(c=Example)
    new_base_obj = base_obj.clone()

    assert base_obj.c == new_base_obj.c


def test_clone_class_rather_than_instance_raises_error():
    """Test clone raises expected error when cloning a class instead of an instance."""
    msg = "You should provide an instance of scikit-learn estimator"
    with pytest.raises(TypeError, match=msg):
        clone(FIXTURE_EXAMPLE)


# Tests of BaseObject pretty printing representation inspired by sklearn
def test_baseobject_repr():
    """Test BaseObject repr works as expected."""
    # Simple test where all parameters are left at defaults
    # Should not see parameters and values in printed representation
    base_obj = FIXTURE_EXAMPLE()
    assert repr(base_obj) == "Example()"

    # Check that we can alter the detail about params that is printed
    # using config_context with ``print_changed_only=False``
    with config_context(print_changed_only=False):
        assert repr(base_obj) == "Example(a='something', b=7, c=None)"

    simple_composite = CompositionDummy(foo=Example())
    assert repr(simple_composite) == "CompositionDummy(foo=Example())"

    long_base_obj_repr = Example(a=["long_params"] * 1000)
    assert len(repr(long_base_obj_repr)) == 543


def test_baseobject_str():
    """Test BaseObject string representation works."""
    base_obj = FIXTURE_EXAMPLE()
    str(base_obj)


def test_baseobject_repr_mimebundle_():
    """Test display configuration controls output."""
    # Checks the display configuration flag controls the json output
    base_obj = FIXTURE_EXAMPLE()
    output = base_obj._repr_mimebundle_()
    assert "text/plain" in output
    assert "text/html" in output

    with config_context(display="text"):
        output = base_obj._repr_mimebundle_()
        assert "text/plain" in output
        assert "text/html" not in output


def test_repr_html_wraps():
    """Test display configuration flag controls the html output."""
    base_obj = FIXTURE_EXAMPLE()

    output = base_obj._repr_html_()
    assert "<style>" in output

    with config_context(display="text"):
        msg = "_repr_html_ is only defined when"
        with pytest.raises(AttributeError, match=msg):
            output = base_obj._repr_html_()
