# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Suite of tests for all objects.

adapted from scikit-learn's and sktime's estimator_checks
"""
import numbers
import types
from copy import deepcopy
from inspect import getfullargspec, isclass, signature
from typing import List

import numpy as np
import pytest

from skbase.base import BaseObject
from skbase.lookup import all_objects
from skbase.testing.utils._conditional_fixtures import (
    create_conditional_fixtures_and_names,
)
from skbase.testing.utils._dependencies import _check_soft_dependencies
from skbase.testing.utils.inspect import _get_args
from skbase.utils.deep_equals import deep_equals

__author__: List[str] = ["fkiraly"]


class BaseFixtureGenerator:
    """Fixture generator for skbase testing functionality.

    Test classes inheriting from this and not overriding pytest_generate_tests
        will have object and scenario fixtures parametrized out of the box.

    Descendants can override:
    object_type_filter: str, class variable; None or scitype string
        e.g., "forecaster", "transformer", "classifier", see BASE_CLASS_SCITYPE_LIST
        which objects are being retrieved and tested
    exclude_objects : str or list of str, or None, default=None
        names of object classes to exclude in retrieval; None = no objects are excluded
    excluded_tests : dict with str keys and list of str values, or None, default=None
        str keys must be object names, value keys must be lists of test names
        names of tests (values) to exclude for object with name as key
        None = no tests are excluded
    valid_tags : list of str or None, default = None
        list of valid tags, None = all tags are valid
    valid_base_types : list of str or None, default = None
        list of valid base types (strings), None = all base types are valid
    fixture_sequence: list of str
        sequence of fixture variable names in conditional fixture generation
    _generate_[variable]: object methods, all (test_name: str, **kwargs) -> list
        generating list of fixtures for fixture variable with name [variable]
            to be used in test with name test_name
        can optionally use values for fixtures earlier in fixture_sequence,
            these must be input as kwargs in a call
    is_excluded: static method (test_name: str, est: class) -> bool
        whether test with name test_name should be excluded for object est
            should be used only for encoding general rules, not individual skips
            individual skips should go on the excluded_tests list
        requires _generate_object_class and _generate_object_instance as is

    Fixtures parametrized
    ---------------------
    object_class: object inheriting from BaseObject
        ranges over object classes not excluded by exclude_objects, excluded_tests
    object_instance: instance of object inheriting from BaseObject
        ranges over object classes not excluded by exclude_objects, excluded_tests
        instances are generated by create_test_instance class method of object_class
    """

    # class variables which can be overridden by descendants
    # ------------------------------------------------------

    # package to search for objects
    # expected type: str, package/module name, relative to python environment root
    package_name = "skbase.tests.mock_package"

    # which object types are generated; None=all, or scitype string like "forecaster"
    object_type_filter = None

    # list of object types (class names) to exclude
    # expected type: list of str, str are class names
    exclude_objects = None

    # list of tests to exclude
    # expected type: dict of lists, key:str, value: List[str]
    # keys are class names of estimators, values are lists of test names to exclude
    excluded_tests = None

    # list of valid tags
    # expected type: list of str, str are tag names
    valid_tags = None

    # list of valid base type names
    # expected type: list of str, str are base type (class) names
    valid_base_types = None

    # which sequence the conditional fixtures are generated in
    fixture_sequence = ["object_class", "object_instance"]

    # which fixtures are indirect, e.g., have an additional pytest.fixture block
    #   to generate an indirect fixture at runtime. Example: object_instance
    #   warning: direct fixtures retain state changes within the same test
    indirect_fixtures = ["object_instance"]

    def pytest_generate_tests(self, metafunc):
        """Test parameterization routine for pytest.

        This uses create_conditional_fixtures_and_names and generator_dict
        to create the fixtures for a mark.parametrize decoration of all tests.
        """
        # get name of the test
        test_name = metafunc.function.__name__

        fixture_sequence = self.fixture_sequence

        fixture_vars = getfullargspec(metafunc.function)[0]

        (
            fixture_param_str,
            fixture_prod,
            fixture_names,
        ) = create_conditional_fixtures_and_names(
            test_name=test_name,
            fixture_vars=fixture_vars,
            generator_dict=self.generator_dict(),
            fixture_sequence=fixture_sequence,
            raise_exceptions=True,
        )

        # determine indirect variables for the parametrization block
        #   this is intersection of self.indirect_vixtures with args in fixture_vars
        indirect_vars = list(set(fixture_vars).intersection(self.indirect_fixtures))

        metafunc.parametrize(
            fixture_param_str,
            fixture_prod,
            ids=fixture_names,
            indirect=indirect_vars,
        )

    def _all_objects(self):
        """Retrieve list of all object classes of type self.object_type_filter."""
        return all_objects(
            object_types=getattr(self, "object_type_filter", None),
            return_names=False,
            exclude_estimators=self.exclude_objects,
            package_name=self.package_name,
        )

    def generator_dict(self):
        """Return dict with methods _generate_[variable] collected in a dict.

        The returned dict is the one required by create_conditional_fixtures_and_names,
            used in this _conditional_fixture plug-in to pytest_generate_tests, above.

        Returns
        -------
        generator_dict : dict, with keys [variable], where
            [variable] are all strings such that self has a static method
                named _generate_[variable](test_name: str, **kwargs)
            value at [variable] is a reference to _generate_[variable]
        """
        gens = [attr for attr in dir(self) if attr.startswith("_generate_")]
        fixts = [gen.replace("_generate_", "") for gen in gens]

        generator_dict = {}
        for var, gen in zip(fixts, gens):
            generator_dict[var] = getattr(self, gen)

        return generator_dict

    def is_excluded(self, test_name, est):
        """Shorthand to check whether test test_name is excluded for object est."""
        if self.excluded_tests is None:
            return False
        else:
            return test_name in self.excluded_tests.get(est.__name__, [])

    # the following functions define fixture generation logic for pytest_generate_tests
    # each function is of signature (test_name:str, **kwargs) -> List of fixtures
    # function with name _generate_[fixture_var] returns list of values for fixture_var
    #   where fixture_var is a fixture variable used in tests
    # the list is conditional on values of other fixtures which can be passed in kwargs

    def _generate_object_class(self, test_name, **kwargs):
        """Return object class fixtures.

        Fixtures parametrized
        ---------------------
        object_class: object inheriting from BaseObject
            ranges over all object classes not excluded by self.excluded_tests
        """
        object_classes_to_test = [
            est for est in self._all_objects() if not self.is_excluded(test_name, est)
        ]
        object_names = [est.__name__ for est in object_classes_to_test]

        return object_classes_to_test, object_names

    def _generate_object_instance(self, test_name, **kwargs):
        """Return object instance fixtures.

        Fixtures parametrized
        ---------------------
        object_instance: instance of object inheriting from BaseObject
            ranges over all object classes not excluded by self.excluded_tests
            instances are generated by create_test_instance class method
        """
        # call _generate_object_class to get all the classes
        object_classes_to_test, _ = self._generate_object_class(test_name=test_name)

        # create instances from the classes
        object_instances_to_test = []
        object_instance_names = []
        # retrieve all object parameters if multiple, construct instances
        for est in object_classes_to_test:
            all_instances_of_est, instance_names = est.create_test_instances_and_names()
            object_instances_to_test += all_instances_of_est
            object_instance_names += instance_names

        return object_instances_to_test, object_instance_names

    # this is executed before each test instance call
    #   if this were not executed, object_instance would keep state changes
    #   within executions of the same test with different parameters
    @pytest.fixture(scope="function")
    def object_instance(self, request):
        """object_instance fixture definition for indirect use."""
        # esetimator_instance is cloned at the start of every test
        return request.param.clone()


class QuickTester:
    """Mixin class which adds the run_tests method to run tests on one object."""

    def run_tests(
        self,
        obj,
        raise_exceptions=False,
        tests_to_run=None,
        fixtures_to_run=None,
        tests_to_exclude=None,
        fixtures_to_exclude=None,
    ):
        """Run all tests on one single object.

        All tests in self are run on the following object type fixtures:
            if est is a class, then object_class = est, and
                object_instance loops over est.create_test_instance()
            if est is an object, then object_class = est.__class__, and
                object_instance = est

        This is compatible with pytest.mark.parametrize decoration,
            but currently only with multiple *single variable* annotations.

        Parameters
        ----------
        obj : object class or object instance
        raise_exceptions : bool, optional, default=False
            whether to return exceptions/failures in the results dict, or raise them
                if False: returns exceptions in returned `results` dict
                if True: raises exceptions as they occur
        tests_to_run : str or list of str, names of tests to run. default = all tests
            sub-sets tests that are run to the tests given here.
        fixtures_to_run : str or list of str, pytest test-fixture combination codes.
            which test-fixture combinations to run. Default = run all of them.
            sub-sets tests and fixtures to run to the list given here.
            If both tests_to_run and fixtures_to_run are provided, runs the *union*,
            i.e., all test-fixture combinations for tests in tests_to_run,
                plus all test-fixture combinations in fixtures_to_run.
        tests_to_exclude : str or list of str, names of tests to exclude. default = None
            removes tests that should not be run, after subsetting via tests_to_run.
        fixtures_to_exclude : str or list of str, fixtures to exclude. default = None
            removes test-fixture combinations that should not be run.
            This is done after subsetting via fixtures_to_run.

        Returns
        -------
        results : dict of results of the tests in self
            keys are test/fixture strings, identical as in pytest, e.g., test[fixture]
            entries are the string "PASSED" if the test passed,
                or the exception raised if the test did not pass
            returned only if all tests pass, or raise_exceptions=False

        Raises
        ------
        if raise_exception=True, raises any exception produced by the tests directly

        Examples
        --------
        >>> from skbase.tests.mock_package.test_mock_package import CompositionDummy
        >>> from skbase.testing.test_all_objects import TestAllObjects
        >>> TestAllObjects().run_tests(
        ...     CompositionDummy,
        ...     tests_to_run="test_constructor"
        ... )
        {'test_constructor[CompositionDummy]': 'PASSED'}
        >>> TestAllObjects().run_tests(
        ...     CompositionDummy, fixtures_to_run="test_repr[CompositionDummy-1]"
        ... )
        {'test_repr[CompositionDummy-1]': 'PASSED'}
        """
        tests_to_run = self._check_none_str_or_list_of_str(
            tests_to_run, var_name="tests_to_run"
        )
        fixtures_to_run = self._check_none_str_or_list_of_str(
            fixtures_to_run, var_name="fixtures_to_run"
        )
        tests_to_exclude = self._check_none_str_or_list_of_str(
            tests_to_exclude, var_name="tests_to_exclude"
        )
        fixtures_to_exclude = self._check_none_str_or_list_of_str(
            fixtures_to_exclude, var_name="fixtures_to_exclude"
        )

        # retrieve tests from self
        test_names = [attr for attr in dir(self) if attr.startswith("test")]

        # we override the generator_dict, by replacing it with temp_generator_dict:
        #  the only object (class or instance) is est, this is overridden
        #  the remaining fixtures are generated conditionally, without change
        temp_generator_dict = deepcopy(self.generator_dict())

        if isclass(obj):
            object_class = obj
        else:
            object_class = type(obj)

        def _generate_object_class(test_name, **kwargs):
            return [object_class], [object_class.__name__]

        def _generate_object_instance(test_name, **kwargs):
            return [obj.clone()], [object_class.__name__]

        def _generate_object_instance_cls(test_name, **kwargs):
            return object_class.create_test_instances_and_names()

        temp_generator_dict["object_class"] = _generate_object_class

        if not isclass(obj):
            temp_generator_dict["object_instance"] = _generate_object_instance
        else:
            temp_generator_dict["object_instance"] = _generate_object_instance_cls
        # override of generator_dict end, temp_generator_dict is now prepared

        # sub-setting to specific tests to run, if tests or fixtures were speified
        if tests_to_run is None and fixtures_to_run is None:
            test_names_subset = test_names
        else:
            test_names_subset = []
            if tests_to_run is not None:
                test_names_subset += list(set(test_names).intersection(tests_to_run))
            if fixtures_to_run is not None:
                # fixture codes contain the test as substring until the first "["
                tests_from_fixt = [fixt.split("[")[0] for fixt in fixtures_to_run]
                test_names_subset += list(set(test_names).intersection(tests_from_fixt))
            test_names_subset = list(set(test_names_subset))

        # sub-setting by removing all tests from tests_to_exclude
        if tests_to_exclude is not None:
            test_names_subset = list(
                set(test_names_subset).difference(tests_to_exclude)
            )

        # the below loops run all the tests and collect the results here:
        results = {}
        # loop A: we loop over all the tests
        for test_name in test_names_subset:
            test_fun = getattr(self, test_name)
            fixture_sequence = self.fixture_sequence

            # all arguments except the first one (self)
            fixture_vars = getfullargspec(test_fun)[0][1:]
            fixture_vars = [var for var in fixture_sequence if var in fixture_vars]

            # this call retrieves the conditional fixtures
            #  for the test test_name, and the object
            _, fixture_prod, fixture_names = create_conditional_fixtures_and_names(
                test_name=test_name,
                fixture_vars=fixture_vars,
                generator_dict=temp_generator_dict,
                fixture_sequence=fixture_sequence,
                raise_exceptions=raise_exceptions,
            )

            # if function is decorated with mark.parametrize, add variable settings
            # NOTE: currently this works only with single-variable mark.parametrize
            if hasattr(test_fun, "pytestmark"):
                if len([x for x in test_fun.pytestmark if x.name == "parametrize"]) > 0:
                    # get the three lists from pytest
                    (
                        pytest_fixture_vars,
                        pytest_fixture_prod,
                        pytest_fixture_names,
                    ) = self._get_pytest_mark_args(test_fun)
                    # add them to the three lists from conditional fixtures
                    fixture_vars, fixture_prod, fixture_names = self._product_fixtures(
                        fixture_vars,
                        fixture_prod,
                        fixture_names,
                        pytest_fixture_vars,
                        pytest_fixture_prod,
                        pytest_fixture_names,
                    )

            # loop B: for each test, we loop over all fixtures
            for params, fixt_name in zip(fixture_prod, fixture_names):
                # this is needed because pytest unwraps 1-tuples automatically
                # but subsequent code assumes params is k-tuple, no matter what k is
                if len(fixture_vars) == 1:
                    params = (params,)
                key = f"{test_name}[{fixt_name}]"
                args = dict(zip(fixture_vars, params))

                # we subset to test-fixtures to run by this, if given
                #  key is identical to the pytest test-fixture string identifier
                if fixtures_to_run is not None and key not in fixtures_to_run:
                    continue
                if fixtures_to_exclude is not None and key in fixtures_to_exclude:
                    continue

                if not raise_exceptions:
                    try:
                        test_fun(**deepcopy(args))
                        results[key] = "PASSED"
                    except Exception as err:
                        results[key] = err
                else:
                    test_fun(**deepcopy(args))
                    results[key] = "PASSED"

        return results

    @staticmethod
    def _check_none_str_or_list_of_str(obj, var_name="obj"):
        """Check that obj is None, str, or list of str, and coerce to list of str."""
        if obj is not None:
            msg = f"{var_name} must be None, str, or list of str"
            if isinstance(obj, str):
                obj = [obj]
            if not isinstance(obj, list):
                raise ValueError(msg)
            if not np.all(isinstance(x, str) for x in obj):
                raise ValueError(msg)
        return obj

    # todo: surely there is a pytest method that can be called instead of this?
    #   find and replace if it exists
    @staticmethod
    def _get_pytest_mark_args(fun):
        """Get args from pytest mark annotation of function.

        Parameters
        ----------
        fun: callable, any function

        Returns
        -------
        pytest_fixture_vars: list of str
            names of args participating in mark.parametrize marks, in pytest order
        pytest_fixt_list: list of tuple
            list of value tuples from the mark parameterization
            i-th value in each tuple corresponds to i-th arg name in pytest_fixture_vars
        pytest_fixt_names: list of str
            i-th element is display name for i-th fixture setting in pytest_fixt_list
        """
        from itertools import product

        marks = [x for x in fun.pytestmark if x.name == "parametrize"]

        def to_str(obj):
            return [str(x) for x in obj]

        def get_id(mark):
            if "ids" in mark.kwargs.keys():
                return mark.kwargs["ids"]
            else:
                return to_str(range(len(mark.args[1])))

        pytest_fixture_vars = [x.args[0] for x in marks]
        pytest_fixt_raw = [x.args[1] for x in marks]
        pytest_fixt_list = product(*pytest_fixt_raw)
        pytest_fixt_names_raw = [get_id(x) for x in marks]
        pytest_fixt_names = product(*pytest_fixt_names_raw)
        pytest_fixt_names = ["-".join(x) for x in pytest_fixt_names]

        return pytest_fixture_vars, pytest_fixt_list, pytest_fixt_names

    @staticmethod
    def _product_fixtures(
        fixture_vars,
        fixture_prod,
        fixture_names,
        pytest_fixture_vars,
        pytest_fixture_prod,
        pytest_fixture_names,
    ):
        """Compute products of two sets of fixture vars, values, names."""
        from itertools import product

        # product of fixture variable names = concatenation
        fixture_vars_return = fixture_vars + pytest_fixture_vars

        # this is needed because pytest unwraps 1-tuples automatically
        # but subsequent code assumes params is k-tuple, no matter what k is
        if len(fixture_vars) == 1:
            fixture_prod = [(x,) for x in fixture_prod]

        # product of fixture products = Cartesian product plus append tuples
        fixture_prod_return = product(fixture_prod, pytest_fixture_prod)
        fixture_prod_return = [sum(x, ()) for x in fixture_prod_return]

        # product of fixture names = Cartesian product plus concat
        fixture_names_return = product(fixture_names, pytest_fixture_names)
        fixture_names_return = ["-".join(x) for x in fixture_names_return]

        return fixture_vars_return, fixture_prod_return, fixture_names_return


class TestAllObjects(BaseFixtureGenerator, QuickTester):
    """Package level tests for BaseObjects."""

    def test_create_test_instance(self, object_class):
        """Check create_test_instance logic and basic constructor functionality.

        create_test_instance and create_test_instances_and_names are the
        key methods used to create test instances in testing.
        If this test does not pass, validity of the other tests cannot be guaranteed.

        Also tests inheritance and super call logic in the constructor.

        Tests that:

        * create_test_instance results in an instance of estimator_class
        * `__init__` calls `super.__init__`
        * `_tags_dynamic` attribute for tag inspection is present after construction
        """
        object_instance = object_class.create_test_instance()

        # Check that init does not construct object of other class than itself
        assert isinstance(object_instance, object_class), (
            "object returned by create_test_instance must be an instance of the class, "
            f"found {type(object_instance)}"
        )

        msg = (
            f"{object_class.__name__}.__init__ should call "
            f"super({object_class.__name__}, self).__init__, "
            "but that does not seem to be the case. Please ensure to call the "
            f"parent class's constructor in {object_class.__name__}.__init__"
        )
        assert hasattr(object_instance, "_tags_dynamic"), msg

    def test_create_test_instances_and_names(self, object_class):
        """Check that create_test_instances_and_names works.

        create_test_instance and create_test_instances_and_names are the
        key methods used to create test instances in testing.
        If this test does not pass, validity of the other tests cannot be guaranteed.

        Tests expected function signature of create_test_instances_and_names.
        """
        objects, names = object_class.create_test_instances_and_names()

        assert isinstance(objects, list), (
            "first return of create_test_instances_and_names must be a list, "
            f"found {type(objects)}"
        )
        assert isinstance(names, list), (
            "second return of create_test_instances_and_names must be a list, "
            f"found {type(names)}"
        )

        assert np.all(isinstance(est, object_class) for est in objects), (
            "list elements of first return returned by create_test_instances_and_names "
            "all must be an instance of the class"
        )

        assert np.all(isinstance(name, names) for name in names), (
            "list elements of second return returned by create_test_instances_and_names"
            " all must be strings"
        )

        assert len(objects) == len(names), (
            "the two lists returned by create_test_instances_and_names must have "
            "equal length"
        )

    def test_object_tags(self, object_class):
        """Check conventions on object tags."""
        assert hasattr(object_class, "get_class_tags")
        all_tags = object_class.get_class_tags()
        assert isinstance(all_tags, dict)
        assert all(isinstance(key, str) for key in all_tags.keys())
        if hasattr(object_class, "_tags"):
            tags = object_class._tags
            msg = (
                f"_tags attribute of class {object_class} must be dict, "
                f"but found {type(tags)}"
            )
            assert isinstance(tags, dict), msg
            assert len(tags) > 0, f"_tags dict of class {object_class} is empty"
            if self.valid_tags is None:
                invalid_tags = tags
            else:
                invalid_tags = [
                    tag for tag in tags.keys() if tag not in self.valid_tags
                ]
            assert len(invalid_tags) == 0, (
                f"_tags of {object_class} contains invalid tags: {invalid_tags}. "
                f"For a list of valid tags, see {self.__class__.__name__}.valid_tags."
            )

        # Avoid ambiguous class attributes
        ambiguous_attrs = ("tags", "tags_")
        for attr in ambiguous_attrs:
            assert not hasattr(object_class, attr), (
                f"Please avoid using the {attr} attribute to disambiguate it from "
                f"object tags."
            )

    def test_inheritance(self, object_class):
        """Check that object inherits from BaseObject."""
        assert issubclass(object_class, BaseObject), (
            f"object: {object_class} " f"is not a sub-class of " f"BaseObject."
        )
        # Usually should inherit only from one BaseObject type
        if self.valid_base_types is not None:
            n_base_types = sum(
                issubclass(object_class, cls) for cls in self.valid_base_types
            )
            assert n_base_types == 1

    # def test_has_common_interface(self, object_class):
    #     """Check object implements the common interface."""
    #     object = object_class

    #     # Check class for type of attribute
    #     assert isinstance(object.is_fitted, property)

    #     required_methods = _list_required_methods(object_class)

    #     for attr in required_methods:
    #         assert hasattr(
    #             object, attr
    #         ), f"object: {object.__name__} does not implement attribute: {attr}"

    def test_no_cross_test_side_effects_part1(self, object_instance):
        """Test that there are no side effects across tests, through object state."""
        object_instance.test__attr = 42

    def test_no_cross_test_side_effects_part2(self, object_instance):
        """Test that there are no side effects across tests, through object state."""
        assert not hasattr(object_instance, "test__attr")

    @pytest.mark.parametrize("a", [True, 42])
    def test_no_between_test_case_side_effects(self, object_instance, a):
        """Test that there are no side effects across instances of the same test."""
        assert not hasattr(object_instance, "test__attr")
        object_instance.test__attr = 42

    @pytest.mark.skipif(
        not _check_soft_dependencies("sklearn", severity="none"),
        reason="skip test if sklearn is not available",
    )  # sklearn is part of the dev dependency set, test should be executed with that
    def test_get_params(self, object_instance):
        """Check that get_params works correctly, against sklearn interface."""
        from sklearn.utils.estimator_checks import (
            check_get_params_invariance as _check_get_params_invariance,
        )

        params = object_instance.get_params()
        assert isinstance(params, dict)
        _check_get_params_invariance(
            object_instance.__class__.__name__, object_instance
        )

    def test_set_params(self, object_instance):
        """Check that set_params works correctly."""
        params = object_instance.get_params()

        msg = f"set_params of {type(object_instance).__name__} does not return self"
        assert object_instance.set_params(**params) is object_instance, msg

        is_equal, equals_msg = deep_equals(
            object_instance.get_params(), params, return_msg=True
        )
        msg = (
            f"get_params result of {type(object_instance).__name__} (x) does not match "
            f"what was passed to set_params (y). Reason for discrepancy: {equals_msg}"
        )
        assert is_equal, msg

    def test_set_params_sklearn(self, object_class):
        """Check that set_params works correctly, mirrors sklearn check_set_params.

        Instead of the "fuzz values" in sklearn's check_set_params,
        we use the other test parameter settings (which are assumed valid).
        This guarantees settings which play along with the __init__ content.
        """
        object_instance = object_class.create_test_instance()
        test_params = object_class.get_test_params()
        if not isinstance(test_params, list):
            test_params = [test_params]

        for params in test_params:
            # we construct the full parameter set for params
            # params may only have parameters that are deviating from defaults
            # in order to set non-default parameters back to defaults
            params_full = object_class.get_param_defaults()
            params_full.update(params)

            msg = f"set_params of {object_class.__name__} does not return self"
            est_after_set = object_instance.set_params(**params_full)
            assert est_after_set is object_instance, msg

            is_equal, equals_msg = deep_equals(
                object_instance.get_params(deep=False), params_full, return_msg=True
            )
            msg = (
                f"get_params result of {object_class.__name__} (x) does not match "
                f"what was passed to set_params (y). "
                f"Reason for discrepancy: {equals_msg}"
            )
            assert is_equal, msg

    def test_clone(self, object_instance):
        """Check that clone method does not raise exceptions and results in a clone.

        A clone of an object x is an object that:

        * has same class and parameters as x
        * is not identical with x
        * is unfitted (even if x was fitted)
        """
        obj_clone = object_instance.clone()
        assert isinstance(obj_clone, type(object_instance))
        assert obj_clone is not object_instance
        if hasattr(obj_clone, "is_fitted"):
            assert not obj_clone.is_fitted

    def test_repr(self, object_instance):
        """Check we can call repr."""
        repr(object_instance)

    def test_constructor(self, object_class):
        """Check that the constructor has sklearn compatible signature and behaviour.

        Based on sklearn check_estimator testing of __init__ logic.
        Uses create_test_instance to create an instance.
        Assumes test_create_test_instance has passed and certified create_test_instance.

        Tests that:

        * constructor has no varargs
        * tests that constructor constructs an instance of the class
        * tests that all parameters are set in init to an attribute of the same name
        * tests that parameter values are always copied to the attribute and not changed
        * tests that default parameters are one of the following:
            None, str, int, float, bool, tuple, function, joblib memory, numpy primitive
            (other type parameters should be None, default handling should be by writing
            the default to attribute of a different name, e.g., my_param_ not my_param)
        """
        msg = f"constructor __init__ of {object_class} should have no varargs"
        assert getfullargspec(object_class.__init__).varkw is None, msg

        obj = object_class.create_test_instance()
        assert isinstance(obj, object_class)

        # Ensure that each parameter is set in init
        init_params = _get_args(type(obj).__init__)
        invalid_attr = set(init_params) - set(vars(obj)) - {"self"}
        assert not invalid_attr, (
            "Object %s should store all parameters"
            " as an attribute during init. Did not find "
            "attributes `%s`." % (obj.__class__.__name__, sorted(invalid_attr))
        )

        # Ensure that init does nothing but set parameters
        # No logic/interaction with other parameters
        def param_filter(p):
            """Identify hyper parameters of an estimator."""
            return p.name != "self" and p.kind not in [p.VAR_KEYWORD, p.VAR_POSITIONAL]

        init_params = [
            p for p in signature(obj.__init__).parameters.values() if param_filter(p)
        ]

        params = obj.get_params()

        # Filter out required parameters with no default value and parameters
        # set for running tests
        required_params = getattr(obj, "_required_parameters", ())

        test_params = obj.get_test_params()
        if isinstance(test_params, list):
            test_params = test_params[0]
        test_params = test_params.keys()

        init_params = [
            param
            for param in init_params
            if param.name not in required_params and param.name not in test_params
        ]

        allowed_param_types = [
            str,
            int,
            float,
            bool,
            tuple,
            type(None),
            np.float64,
            types.FunctionType,
        ]
        if _check_soft_dependencies("joblib", severity="none"):
            from joblib import Memory

            allowed_param_types += [Memory]

        for param in init_params:
            assert param.default != param.empty, (
                "parameter `%s` for %s has no default value and is not "
                "included in `_required_parameters`"
                % (param.name, obj.__class__.__name__)
            )
            if type(param.default) is type:
                assert param.default in [np.float64, np.int64]
            else:
                assert type(param.default) in allowed_param_types

            param_value = params[param.name]
            if isinstance(param_value, np.ndarray):
                np.testing.assert_array_equal(param_value, param.default)
            else:
                if bool(
                    isinstance(param_value, numbers.Real) and np.isnan(param_value)
                ):
                    # Allows to set default parameters to np.nan
                    assert param_value is param.default, param.name
                else:
                    assert param_value == param.default, param.name

    def test_valid_object_class_tags(self, object_class):
        """Check that object class tags are in self.valid_tags."""
        if self.valid_tags is None:
            return None
        for tag in object_class.get_class_tags().keys():
            assert tag in self.valid_tags

    def test_valid_object_tags(self, object_instance):
        """Check that object tags are in self.valid_tags."""
        if self.valid_tags is None:
            return None
        for tag in object_instance.get_tags().keys():
            assert tag in self.valid_tags
