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

__author__ = ["fkiraly", "RNKuhns"]

__all__ = [
    "test_get_class_tags",
    "test_get_class_tag",
    "test_get_tags",
    "test_get_tag",
    "test_set_tags",
    "test_set_tags_works_with_missing_tags_dynamic_attribute",
    "test_clone_tags",
    "test_components",
    "test_components_raises_error_base_class_is_not_class",
    "test_components_raises_error_base_class_is_not_baseobject_subclass",
    "test_reset",
    "test_reset_composite",
    "test_get_init_signature",
    "test_get_init_signature_raises_error_for_invalid_signature",
    "test_get_param_names",
    "test_get_params",
    "test_set_params",
    "test_set_params_raises_error_non_existent_param",
    "test_set_params_raises_error_non_interface_composite",
    "test_raises_on_get_params_for_param_arg_not_assigned_to_attribute",
    "test_set_params_with_no_param_to_set_returns_object",
    "test_clone",
    "test_clone_2",
    "test_clone_class_rather_than_instance_raises_error",
    "test_clone_estimator_types",
    "test_clone_raises_error_for_nonconforming_objects",
    "test_baseobject_repr",
    "test_baseobject_str",
    "test_baseobject_repr_mimebundle_",
    "test_repr_html_wraps",
]
import inspect
from copy import deepcopy

import pytest
from sklearn import config_context

# TODO: Update with import of skbase clone function once implemented
from sklearn.base import clone

from skbase import BaseObject

# TODO: Determine if we need to add sklearn style test of
# test_set_params_passes_all_parameters


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
        super().__init__()

    def some_method():
        """To be implemented by child class."""
        pass


class ExampleChild(Example):
    """Child of Example class."""

    def some_method():
        """Child class' implementation."""
        pass

    def some_other_method():
        """To be implemented in the child class."""


class RequiredParam(BaseObject):
    """BaseObject class with _required_parameters."""

    _required_parameters = ["a"]

    def __init__self(self, a, b=7):
        self.a = a
        self.b = b


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
FIXTURE_EXAMPLE_EXPECTED_PARAMS = {"a": "something", "b": 7, "c": None}
FIXTURE_EXAMPLE_EXPECTED_PARAM_NAMES = sorted([*FIXTURE_EXAMPLE_EXPECTED_PARAMS])
FIXTURE_EXAMPLE_CHILD = ExampleChild
FIXTURE_REQUIRED_PARAM = RequiredParam
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


def test_set_tags_works_with_missing_tags_dynamic_attribute():
    """Test set_tags will still work if _tags_dynamic is missing."""
    base_obj = deepcopy(FIXTURE_OBJECT)
    delattr(base_obj, "_tags_dynamic")
    assert not hasattr(base_obj, "_tags_dynamic")
    base_obj.set_tags(some_tag="something")
    tags = base_obj.get_tags()
    assert hasattr(base_obj, "_tags_dynamic")
    assert "some_tag" in tags and tags["some_tag"] == "something"


def test_clone_tags():
    """Test clone_tags works as expected."""

    class TestClass(BaseObject):
        _tags = {"some_tag": True, "another_tag": 37}

    class AnotherTestClass(BaseObject):
        pass

    # Simple example of cloning all tags with no tags overlapping
    base_obj = FIXTURE_EXAMPLE()
    test_obj = TestClass()
    assert base_obj.get_tags() == {}
    base_obj.clone_tags(test_obj)
    assert base_obj.get_class_tags() == {}
    assert base_obj.get_tags() == test_obj.get_tags()

    # Simple examples cloning named tags with no tags overlapping
    base_obj = FIXTURE_EXAMPLE()
    test_obj = TestClass()
    assert base_obj.get_tags() == {}
    base_obj.clone_tags(test_obj, tag_names="some_tag")
    assert base_obj.get_class_tags() == {}
    assert base_obj.get_tags() == {"some_tag": True}
    base_obj.clone_tags(test_obj, tag_names=["another_tag"])
    assert base_obj.get_class_tags() == {}
    assert base_obj.get_tags() == test_obj.get_tags()

    # Overlapping tag example where there is tags in each object that aren't
    # in the other object
    another_base_obj = AnotherTestClass()
    another_base_obj.set_tags(some_tag=False, a_new_tag="words")
    another_base_obj_tags = another_base_obj.get_tags()
    test_obj = TestClass()
    assert test_obj.get_tags() == TestClass.get_class_tags()
    test_obj.clone_tags(another_base_obj)
    test_obj_tags = test_obj.get_tags()
    assert test_obj.get_class_tags() == TestClass.get_class_tags()
    # Verify all tags in another_base_obj were cloned into test_obj
    for tag in another_base_obj_tags:
        assert test_obj_tags.get(tag) == another_base_obj_tags[tag]
    # Verify tag that was in test_obj but not another_base_obj still has same value
    # and there aren't any other tags
    assert (
        "another_tag" in test_obj_tags
        and test_obj_tags["another_tag"] == 37
        and len(test_obj_tags) == 3
    )

    # Overlapping tag example using named tags in clone
    another_base_obj = AnotherTestClass()
    another_base_obj.set_tags(some_tag=False, a_new_tag="words")
    another_base_obj_tags = another_base_obj.get_tags()
    test_obj = TestClass()
    assert test_obj.get_tags() == TestClass.get_class_tags()
    test_obj.clone_tags(another_base_obj, tag_names=["a_new_tag"])
    test_obj_tags = test_obj.get_tags()
    assert test_obj.get_class_tags() == TestClass.get_class_tags()
    assert test_obj_tags.get("a_new_tag") == "words"


# Test composition related interface functionality
class CompositionDummy(BaseObject):
    """Potentially composite object, for testing."""

    def __init__(self, foo, bar=84):
        self.foo = foo
        self.foo_ = deepcopy(foo)
        self.bar = bar
        super().__init__()


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
    comp_comps_baseobject_filter = composite._components(BaseObject)
    comp_comps_filter = composite._components(FIXTURE_EXAMPLE)

    assert isinstance(non_comp_comps, dict)
    assert set(non_comp_comps.keys()) == set()

    assert isinstance(comp_comps, dict)
    assert set(comp_comps.keys()) == {"foo_"}
    assert comp_comps["foo_"] == composite.foo_
    assert comp_comps["foo_"] != composite.foo

    assert comp_comps == comp_comps_baseobject_filter
    assert comp_comps_filter == {}


def test_components_raises_error_base_class_is_not_class():
    """Test _component method raises error if base_class param is not class."""
    non_composite = CompositionDummy(foo=42)
    composite = CompositionDummy(foo=non_composite)
    with pytest.raises(
        TypeError, match="base_class must be a class, but found <class 'int'>"
    ):
        composite._components(7)

    with pytest.raises(
        TypeError,
        match="base_class must be a class, but found <class 'skbase._base.BaseObject'>",
    ):
        composite._components(BaseObject())


def test_components_raises_error_base_class_is_not_baseobject_subclass():
    """Test _component method raises error if base_class is not BaseObject subclass."""

    class SomeClass:
        pass

    composite = CompositionDummy(foo=SomeClass())
    with pytest.raises(TypeError, match="base_class must be a subclass of BaseObject"):
        composite._components(SomeClass)


class ResetTester(BaseObject):

    clsvar = 210

    def __init__(self, a, b=42):
        self.a = a
        self.b = b
        self.c = 84
        super().__init__()

    def foo(self, d=126):
        self.d = deepcopy(d)
        self._d = deepcopy(d)
        self.d_ = deepcopy(d)
        self.f__o__o = 252


# Test parameter interface (get_params, set_params, reset and related methods)
# Some tests of get_params and set_params are adapted from sklearn tests
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


class NoParamInterface:
    def __init__(self, a=7, b=12):
        self.a = a
        self.b = b


def test_get_params():
    """Test get_params returns expected parameters."""
    # Simple test of returned params
    base_obj = FIXTURE_EXAMPLE()
    params = base_obj.get_params()
    assert params == FIXTURE_EXAMPLE_EXPECTED_PARAMS

    composite = CompositionDummy(foo=base_obj, bar=84)
    params = composite.get_params()
    assert "foo__a" in params and "foo__b" in params and "foo__c" in params
    assert "bar" in params and params["bar"] == 84
    assert "foo" in params and isinstance(params["foo"], FIXTURE_EXAMPLE)
    assert "foo__a" not in composite.get_params(deep=False)

    # Since NoParamInterface does not have get_params we should just return
    # "foo" and "bar" in params and no other parameters
    composite = CompositionDummy(foo=NoParamInterface())
    params = composite.get_params()
    assert "foo" in params and "bar" in params and len(params) == 2


def test_set_params():
    """Test set_params works as expected."""
    # Simple case of setting a parameter
    base_obj = FIXTURE_EXAMPLE()
    base_obj.set_params(b="updated param value")
    expected_params = deepcopy(FIXTURE_EXAMPLE_EXPECTED_PARAMS)
    expected_params["b"] = "updated param value"
    assert base_obj.get_params() == expected_params

    # Setting parameter of a composite class
    composite = CompositionDummy(foo=FIXTURE_EXAMPLE(), bar=84)
    composite.set_params(bar=95, foo__b="updated param value")
    params = composite.get_params()
    assert params["bar"] == 95
    assert (
        params["foo__b"] == "updated param value"
        and composite.foo.b == "updated param value"
    )


def test_set_params_raises_error_non_existent_param():
    """Test set_params raises an error when passed a non-existent parameter name."""
    # non-existing parameter in svc
    base_obj = FIXTURE_EXAMPLE()
    with pytest.raises(ValueError):
        base_obj.set_params(non_existant_param="updated param value")

    # non-existing parameter of composite
    composite = CompositionDummy(foo=FIXTURE_EXAMPLE(), bar=84)
    with pytest.raises(ValueError):
        composite.set_params(foo__non_existant_param=True)


def test_set_params_raises_error_non_interface_composite():
    """Test set_params raises error when setting param of non-conforming composite."""
    # When a composite is made up of a class that doesn't have the BaseObject
    # parameter interface, we should get a AttributeError when trying to
    # set the composite's params
    composite = CompositionDummy(foo=NoParamInterface())
    with pytest.raises(AttributeError):
        composite.set_params(foo__a=88)


def test_raises_on_get_params_for_param_arg_not_assigned_to_attribute():
    """Test get_params raises error if param not assigned to same named attribute."""

    class BadObject(BaseObject):
        # Here we don't assign param to self.param as expected in interface
        def __init__(self, param=5):
            pass

    est = BadObject()
    msg = "'BadObject' object has no attribute 'param'"

    with pytest.raises(AttributeError, match=msg):
        est.get_params()


def test_set_params_with_no_param_to_set_returns_object():
    """Test set_params correctly returns self when no parameters are set."""
    base_obj = FIXTURE_EXAMPLE()
    orig_params = deepcopy(base_obj.get_params())
    base_obj_set_params = base_obj.set_params()
    assert (
        isinstance(base_obj_set_params, FIXTURE_EXAMPLE)
        and base_obj_set_params.get_params() == orig_params
    )


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
    with config_context(display="diagram"):
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

    with config_context(display="diagram"):
        output = base_obj._repr_html_()
        assert "<style>" in output

    with config_context(display="text"):
        msg = "_repr_html_ is only defined when"
        with pytest.raises(AttributeError, match=msg):
            output = base_obj._repr_html_()


# Test BaseObject's ability to generate test instances
def test_get_test_params():
    """Test get_test_params returns empty dictionary."""
    base_obj = FIXTURE_EXAMPLE()
    test_params = base_obj.get_test_params()
    assert isinstance(test_params, dict) and len(test_params) == 0


def test_get_test_params_raises_error_when_params_required():
    """Test get_test_params raises an error when parameters are required."""
    with pytest.raises(ValueError):
        FIXTURE_REQUIRED_PARAM().get_test_params()


def test_create_test_instance():
    """Test first that create_test_instance logic works."""
    base_obj = FIXTURE_EXAMPLE.create_test_instance()

    # Check that init does not construct object of other class than itself
    assert isinstance(base_obj, FIXTURE_EXAMPLE().__class__), (
        "Object returned by create_test_instance must be an instance of the class, "
        f"but found {type(base_obj)}."
    )

    msg = (
        f"{FIXTURE_EXAMPLE.__name__}.__init__ should call "
        f"super({FIXTURE_EXAMPLE.__name__}, self).__init__, "
        "but that does not seem to be the case. Please ensure to call the "
        f"parent class's constructor in {FIXTURE_EXAMPLE.__name__}.__init__"
    )
    assert hasattr(base_obj, "_tags_dynamic"), msg


def test_create_test_instances_and_names():
    """Test that create_test_instances_and_names works."""
    base_objs, names = FIXTURE_EXAMPLE.create_test_instances_and_names()

    assert isinstance(base_objs, list), (
        "First return of create_test_instances_and_names must be a list, "
        f"but found {type(base_objs)}."
    )
    assert isinstance(names, list), (
        "Second return of create_test_instances_and_names must be a list, "
        f"but found {type(names)}."
    )

    assert all([isinstance(est, FIXTURE_EXAMPLE().__class__) for est in base_objs]), (
        "List elements of first return returned by create_test_instances_and_names "
        "all must be an instance of the class"
    )

    assert all([isinstance(name, str) for name in names]), (
        "List elements of second return returned by create_test_instances_and_names"
        " all must be strings."
    )

    assert len(base_objs) == len(names), (
        "The two lists returned by create_test_instances_and_names must have "
        "equal length."
    )


# Tests _has_implementation_of interface
def test_has_implementation_of():
    """Test _has_implementation_of detects methods in class with overrides in mro."""
    base_obj = FIXTURE_EXAMPLE_CHILD()
    # When the class overrides a parent classes method should return True
    assert base_obj._has_implementation_of("some_method")
    # When class implements method first time it shoudl return False
    assert not base_obj._has_implementation_of("some_other_method")

    # If the method is defined the first time in the parent class it should not
    # return _has_implementation_of == True
    base_obj_parent = FIXTURE_EXAMPLE()
    assert not base_obj_parent._has_implementation_of("some_method")
