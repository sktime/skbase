# -*- coding: utf-8 -*-
"""Common functionality for skbase unit tests."""
from typing import List

from skbase.base import BaseEstimator, BaseObject

__all__: List[str] = [
    "SKBASE_BASE_CLASSES",
    "SKBASE_MODULES",
    "SKBASE_PUBLIC_MODULES",
    "SKBASE_PUBLIC_CLASSES_BY_MODULE",
    "SKBASE_CLASSES_BY_MODULE",
    "SKBASE_PUBLIC_FUNCTIONS_BY_MODULE",
    "SKBASE_FUNCTIONS_BY_MODULE",
]
__author__: List[str] = ["fkiraly", "RNKuhns"]

SKBASE_BASE_CLASSES = (BaseObject, BaseEstimator)
SKBASE_MODULES = (
    "skbase",
    "skbase._exceptions",
    "skbase._nopytest_tests",
    "skbase.base",
    "skbase.base._base",
    "skbase.base._clone_base",
    "skbase.base._clone_plugins",
    "skbase.base._meta",
    "skbase.base._pretty_printing",
    "skbase.base._pretty_printing._object_html_repr",
    "skbase.base._pretty_printing._pprint",
    "skbase.base._tagmanager",
    "skbase.lookup",
    "skbase.lookup.tests",
    "skbase.lookup.tests.test_lookup",
    "skbase.lookup._lookup",
    "skbase.testing",
    "skbase.testing.test_all_objects",
    "skbase.testing.utils",
    "skbase.testing.utils._conditional_fixtures",
    "skbase.testing.utils.inspect",
    "skbase.testing.utils.tests",
    "skbase.testing.utils.tests.test_deep_equals",
    "skbase.tests",
    "skbase.tests.conftest",
    "skbase.tests.test_base",
    "skbase.tests.test_baseestimator",
    "skbase.tests.mock_package.test_mock_package",
    "skbase.utils",
    "skbase.utils._check",
    "skbase.utils._iter",
    "skbase.utils._nested_iter",
    "skbase.utils._utils",
    "skbase.utils.deep_equals",
    "skbase.utils.deep_equals._common",
    "skbase.utils.deep_equals._deep_equals",
    "skbase.utils.dependencies",
    "skbase.utils.dependencies._dependencies",
    "skbase.utils.dependencies._import",
    "skbase.utils.random_state",
    "skbase.utils.stderr_mute",
    "skbase.utils.stdout_mute",
    "skbase.validate",
    "skbase.validate._named_objects",
    "skbase.validate._types",
)
SKBASE_PUBLIC_MODULES = (
    "skbase",
    "skbase.base",
    "skbase.lookup",
    "skbase.lookup.tests",
    "skbase.lookup.tests.test_lookup",
    "skbase.testing",
    "skbase.testing.test_all_objects",
    "skbase.testing.utils",
    "skbase.testing.utils.inspect",
    "skbase.testing.utils.tests",
    "skbase.testing.utils.tests.test_deep_equals",
    "skbase.tests",
    "skbase.tests.conftest",
    "skbase.tests.test_base",
    "skbase.tests.test_baseestimator",
    "skbase.tests.mock_package.test_mock_package",
    "skbase.utils",
    "skbase.utils.deep_equals",
    "skbase.utils.dependencies",
    "skbase.utils.random_state",
    "skbase.utils.stderr_mute",
    "skbase.utils.stdout_mute",
    "skbase.validate",
)
SKBASE_PUBLIC_CLASSES_BY_MODULE = {
    "skbase._exceptions": ("FixtureGenerationError", "NotFittedError"),
    "skbase.base": (
        "BaseEstimator",
        "BaseMetaEstimator",
        "BaseMetaEstimatorMixin",
        "BaseMetaObject",
        "BaseMetaObjectMixin",
        "BaseObject",
    ),
    "skbase.base._base": ("BaseEstimator", "BaseObject"),
    "skbase.base._clone_plugins": ("BaseCloner",),
    "skbase.base._meta": (
        "BaseMetaObject",
        "BaseMetaObjectMixin",
        "BaseMetaEstimator",
        "BaseMetaEstimatorMixin",
    ),
    "skbase.base._pretty_printing._pprint": ("KeyValTuple", "KeyValTupleParam"),
    "skbase.lookup._lookup": ("StdoutMuteNCatchMNF",),
    "skbase.testing": ("BaseFixtureGenerator", "QuickTester", "TestAllObjects"),
    "skbase.testing.test_all_objects": (
        "BaseFixtureGenerator",
        "QuickTester",
        "TestAllObjects",
    ),
    "skbase.utils.stderr_mute": ("StderrMute",),
    "skbase.utils.stdout_mute": ("StdoutMute",),
}
SKBASE_CLASSES_BY_MODULE = SKBASE_PUBLIC_CLASSES_BY_MODULE.copy()
SKBASE_CLASSES_BY_MODULE.update(
    {
        "skbase.base._clone_plugins": (
            "BaseCloner",
            "_CloneClass",
            "_CloneSkbase",
            "_CloneSklearn",
            "_CloneDict",
            "_CloneListTupleSet",
            "_CloneGetParams",
            "_CloneCatchAll",
        ),
        "skbase.base._meta": (
            "BaseMetaObject",
            "BaseMetaObjectMixin",
            "BaseMetaEstimator",
            "BaseMetaEstimatorMixin",
            "_MetaObjectMixin",
            "_MetaTagLogicMixin",
        ),
        "skbase.base._pretty_printing._object_html_repr": ("_VisualBlock",),
        "skbase.base._pretty_printing._pprint": (
            "KeyValTuple",
            "KeyValTupleParam",
            "_BaseObjectPrettyPrinter",
        ),
        "skbase.base._tagmanager": ("_FlagManager",),
    }
)
SKBASE_PUBLIC_FUNCTIONS_BY_MODULE = {
    "skbase.lookup": ("all_objects", "get_package_metadata"),
    "skbase.lookup._lookup": ("all_objects", "get_package_metadata"),
    "skbase.testing.utils._conditional_fixtures": (
        "create_conditional_fixtures_and_names",
    ),
    "skbase.validate": (
        "check_sequence_named_objects",
        "check_sequence",
        "check_type",
        "is_named_object_tuple",
        "is_sequence",
        "is_sequence_named_objects",
    ),
    "skbase.validate._named_objects": (
        "check_sequence_named_objects",
        "is_named_object_tuple",
        "is_sequence_named_objects",
    ),
    "skbase.utils": (
        "check_random_state",
        "deep_equals",
        "flatten",
        "is_flat",
        "make_strings_unique",
        "sample_dependent_seed",
        "set_random_state",
        "subset_dict_keys",
        "unflat_len",
        "unflatten",
    ),
    "skbase.utils._iter": ("make_strings_unique",),
    "skbase.utils._nested_iter": (
        "flatten",
        "is_flat",
        "unflat_len",
        "unflatten",
    ),
    "skbase.utils._utils": ("subset_dict_keys",),
    "skbase.utils.deep_equals": ("deep_equals",),
    "skbase.utils.deep_equals._deep_equals": ("deep_equals", "deep_equals_custom"),
    "skbase.utils.random_state": (
        "check_random_state",
        "sample_dependent_seed",
        "set_random_state",
    ),
    "skbase.validate._types": ("check_sequence", "check_type", "is_sequence"),
}
SKBASE_FUNCTIONS_BY_MODULE = SKBASE_PUBLIC_FUNCTIONS_BY_MODULE.copy()
SKBASE_FUNCTIONS_BY_MODULE.update(
    {
        "skbase.base._clone_base": {"_check_clone", "_clone"},
        "skbase.base._clone_plugins": ("_default_clone",),
        "skbase.base._pretty_printing._object_html_repr": (
            "_get_visual_block",
            "_object_html_repr",
            "_write_base_object_html",
            "_write_label_html",
        ),
        "skbase.base._pretty_printing._pprint": ("_changed_params", "_safe_repr"),
        "skbase.lookup._lookup": (
            "_determine_module_path",
            "_get_return_tags",
            "_is_ignored_module",
            "all_objects",
            "_is_non_public_module",
            "get_package_metadata",
            "_make_dataframe",
            "_walk",
            "_filter_by_tags",
            "_filter_by_class",
            "_import_module",
            "_check_object_types",
            "_get_module_info",
            "_coerce_to_tuple",
        ),
        "skbase.testing.utils.inspect": ("_get_args",),
        "skbase.utils._check": ("_is_scalar_nan",),
        "skbase.utils.dependencies": (
            "_check_soft_dependencies",
            "_check_python_version",
            "_check_estimator_deps",
        ),
        "skbase.utils.dependencies._import": ("_safe_import",),
        "skbase.utils._iter": (
            "_format_seq_to_str",
            "_remove_type_text",
            "_scalar_to_seq",
            "make_strings_unique",
        ),
        "skbase.utils._nested_iter": (
            "flatten",
            "is_flat",
            "_remove_single",
            "unflat_len",
            "unflatten",
        ),
        "skbase.utils._utils": ("subset_dict_keys",),
        "skbase.utils.deep_equals": ("deep_equals",),
        "skbase.utils.deep_equals._common": ("_make_ret", "_ret"),
        "skbase.utils.deep_equals._deep_equals": (
            "_coerce_list",
            "_dict_equals",
            "_fh_equals_plugin",
            "_is_npnan",
            "_is_npndarray",
            "_is_pandas",
            "_numpy_equals_plugin",
            "_pandas_equals",
            "_pandas_equals_plugin",
            "_safe_any_unequal",
            "_safe_len",
            "_softdep_available",
            "_tuple_equals",
            "deep_equals",
            "deep_equals_custom",
        ),
        "skbase.utils.dependencies._dependencies": (
            "_check_soft_dependencies",
            "_check_python_version",
            "_check_env_marker",
            "_check_estimator_deps",
            "_get_pkg_version",
            "_get_installed_packages",
            "_normalize_requirement",
            "_raise_at_severity",
        ),
        "skbase.utils.random_state": (
            "check_random_state",
            "sample_dependent_seed",
            "set_random_state",
        ),
        "skbase.validate._named_objects": (
            "check_sequence_named_objects",
            "is_named_object_tuple",
            "is_sequence_named_objects",
            "_named_baseobject_error_msg",
        ),
        "skbase.validate._types": (
            "check_sequence",
            "check_type",
            "is_sequence",
            "_convert_scalar_seq_type_input_to_tuple",
        ),
    }
)


# Fixture class for testing tag system
class Parent(BaseObject):
    """Parent class to test BaseObject's usage."""

    _tags = {"A": "1", "B": 2, "C": 1234, "3": "D"}

    def __init__(self, a="something", b=7, c=None):
        """Initialize the class."""
        self.a = a
        self.b = b
        self.c = c
        super().__init__()

    def some_method(self):
        """To be implemented by child class."""
        pass


# Fixture class for testing tag system, child overrides tags
class Child(Parent):
    """Child class that is child of FixtureClassParent."""

    _tags = {"A": 42, "3": "E"}
    __author__ = ["fkiraly", "RNKuhns"]

    def some_method(self):
        """Child class' implementation."""
        pass

    def some_other_method(self):
        """To be implemented in the child class."""
        pass


# Fixture class for testing tag system, child overrides tags
class ClassWithABTrue(Parent):
    """Child class that sets A, B tags to True."""

    _tags = {"A": True, "B": True}
    __author__ = ["fkiraly", "RNKuhns"]

    def some_method(self):
        """Child class' implementation."""
        pass

    def some_other_method(self):
        """To be implemented in the child class."""
        pass
