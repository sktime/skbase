# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for skbase lookup functionality."""
# Elements of the lookup tests reuse code developed in sktime. These elements
# are copyrighted by the sktime developers, BSD-3-Clause License. For
# conditions see https://github.com/sktime/sktime/blob/main/LICENSE
import importlib
import pathlib
import sys
from copy import deepcopy
from types import ModuleType
from typing import List

import pandas as pd
import pytest

from skbase.base import BaseEstimator, BaseObject
from skbase.base._base import TagAliaserMixin
from skbase.lookup import all_objects, get_package_metadata
from skbase.lookup._lookup import (
    _determine_module_path,
    _filter_by_class,
    _filter_by_tags,
    _get_return_tags,
    _import_module,
    _is_ignored_module,
    _is_non_public_module,
    _walk,
)
from skbase.tests.conftest import (
    SKBASE_BASE_CLASSES,
    SKBASE_CLASSES_BY_MODULE,
    SKBASE_FUNCTIONS_BY_MODULE,
    SKBASE_MODULES,
    SKBASE_PUBLIC_CLASSES_BY_MODULE,
    SKBASE_PUBLIC_FUNCTIONS_BY_MODULE,
    SKBASE_PUBLIC_MODULES,
    ClassWithABTrue,
    Parent,
)
from skbase.tests.mock_package.test_mock_package import (
    MOCK_PACKAGE_OBJECTS,
    CompositionDummy,
    NotABaseObject,
)

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = []


MODULE_METADATA_EXPECTED_KEYS = (
    "path",
    "name",
    "classes",
    "functions",
    "__all__",
    "authors",
    "is_package",
    "contains_concrete_class_implementations",
    "contains_base_classes",
    "contains_base_objects",
)

SAMPLE_METADATA = {
    "some_module": {
        "path": "//some_drive/some_path/",
        "name": "some_module",
        "classes": {
            CompositionDummy.__name__: {
                "klass": CompositionDummy,
                "name": CompositionDummy.__name__,
                "description": "This class does something.",
                "tags": {},
                "is_concrete_implementation": True,
                "is_base_class": False,
                "is_base_object": True,
                "authors": "JDoe",
                "module_name": "some_module",
            },
        },
        "functions": {
            get_package_metadata.__name__: {
                "func": get_package_metadata,
                "name": get_package_metadata.__name__,
                "description": "This function does stuff.",
                "module_name": "some_module",
            },
        },
        "__all__": ["SomeClass", "some_function"],
        "authors": "JDoe",
        "is_package": True,
        "contains_concrete_class_implementations": True,
        "contains_base_classes": False,
        "contains_base_objects": True,
    }
}
MOD_NAMES = {
    "public": (
        "skbase",
        "skbase.lookup",
        "some_module.some_sub_module",
        "tests.test_mock_package",
    ),
    "non_public": (
        "skbase.lookup._lookup",
        "some_module._some_non_public_sub_module",
        "_skbase",
    ),
}
REQUIRED_CLASS_METADATA_KEYS = [
    "klass",
    "name",
    "description",
    "tags",
    "is_concrete_implementation",
    "is_base_class",
    "is_base_object",
    "authors",
    "module_name",
]
REQUIRED_FUNCTION_METADATA_KEYS = ["func", "name", "description", "module_name"]


@pytest.fixture
def mod_names():
    """Pytest fixture to return module names for tests."""
    return MOD_NAMES


@pytest.fixture
def fixture_test_lookup_mod_path():
    """Fixture path to the lookup module determined from this file's path."""
    return pathlib.Path(__file__).parent.parent


@pytest.fixture
def fixture_skbase_root_path(fixture_test_lookup_mod_path):
    """Fixture to root path of skbase package."""
    return fixture_test_lookup_mod_path.parent


@pytest.fixture
def fixture_sample_package_metadata():
    """Fixture of sample module metadata."""
    return SAMPLE_METADATA


def _check_package_metadata_result(results):
    """Check output of get_package_metadata is expected type."""
    if not (isinstance(results, dict) and all(isinstance(k, str) for k in results)):
        return False
    for k, mod_metadata in results.items():
        if not isinstance(mod_metadata, dict):
            return False
        # Verify expected metadata keys are in the module's metadata dict
        if not all(k in mod_metadata for k in MODULE_METADATA_EXPECTED_KEYS):
            return False
        # Verify keys with string values have string values
        if not all(
            isinstance(mod_metadata[k], str) for k in ("path", "name", "authors")
        ):
            return False
        # Verify keys with bool values have bool values
        if not all(
            isinstance(mod_metadata[k], bool)
            for k in (
                "is_package",
                "contains_concrete_class_implementations",
                "contains_base_classes",
                "contains_base_objects",
            )
        ):
            return False
        # Verify __all__ key
        if not (
            isinstance(mod_metadata["__all__"], list)
            and all(isinstance(k, str) for k in mod_metadata["__all__"])
        ):
            return False
        # Verify classes key is a dict that contains string keys and dict values
        if not (
            isinstance(mod_metadata["classes"], dict)
            and all(
                isinstance(k, str) and isinstance(v, dict)
                for k, v in mod_metadata["classes"].items()
            )
        ):
            return False
        # Then verify sub-dict values for each class have required keys
        elif not all(
            k in c_meta
            for c_meta in mod_metadata["classes"].values()
            for k in REQUIRED_CLASS_METADATA_KEYS
        ):
            return False
        # Verify functions key is a dict that contains string keys and dict values
        if not (
            isinstance(mod_metadata["functions"], dict)
            and all(
                isinstance(k, str) and isinstance(v, dict)
                for k, v in mod_metadata["functions"].items()
            )
        ):
            return False
        # Then verify sub-dict values for each function have required keys
        elif not all(
            k in f_meta
            for f_meta in mod_metadata["functions"].values()
            for k in REQUIRED_FUNCTION_METADATA_KEYS
        ):
            return False
    # Otherwise return True
    return True


def _check_all_object_output_types(
    objs, as_dataframe=True, return_names=True, return_tags=None
):
    """Check that all_objects output has expected types."""
    # We expect at least one object to be returned
    assert len(objs) > 0
    if as_dataframe:
        expected_obj_column = 1 if return_names else 0
        expected_columns = 2 if return_names else 1
        if isinstance(return_tags, str):
            expected_columns += 1
        elif isinstance(return_tags, list):
            expected_columns += len(return_tags)
        assert isinstance(objs, pd.DataFrame) and objs.shape[1] == expected_columns
        # Verify all objects in the object columns are BaseObjects
        assert (
            objs.iloc[:, expected_obj_column]
            .apply(issubclass, args=(BaseObject,))
            .all()
        )
        # If names are returned, verify they are all strings
        if return_names:
            assert objs.iloc[:, 0].apply(isinstance, args=(str,)).all()
            assert (
                objs.iloc[:, 0] == objs.iloc[:, 1].apply(lambda x: x.__name__)
            ).all()

    else:
        # Should return a list
        assert isinstance(objs, list)
        # checks return type specification (see docstring)
        for obj in objs:
            # return is list of objects if no names or tags requested
            if not return_names and return_tags is None:
                assert issubclass(obj, BaseObject)
            elif return_names:
                assert isinstance(obj, tuple)
                assert isinstance(obj[0], str)
                assert issubclass(obj[1], BaseObject)
                assert obj[0] == obj[1].__name__
                if return_tags is None:
                    assert len(obj) == 2
                elif isinstance(return_tags, str):
                    assert len(obj) == 3
                else:
                    assert len(obj) == 2 + len(return_tags)


def test_check_package_metadata_result(fixture_sample_package_metadata):
    """Test _check_package_metadata_result works as expected."""

    def _update_mod_metadata(metadata, dict_update):
        mod_metadata = deepcopy(metadata)
        # mod_metadata["some_module"] = mod_metadata["some_module"].copy()
        mod_metadata["some_module"].update(dict_update.copy())
        return mod_metadata

    assert _check_package_metadata_result(fixture_sample_package_metadata) is True
    # Input not dict returns False
    assert _check_package_metadata_result(7) is False
    # Input that doesn't have string keys mapping to dicts is False
    assert _check_package_metadata_result({"something": 7}) is False
    # If keys map to dicts that don't have expected keys then False
    assert _check_package_metadata_result({"something": {"something_else": 7}}) is False
    # Make sure keys with wrong type through errors
    mod_metadata = _update_mod_metadata(fixture_sample_package_metadata, {"name": 7})
    assert _check_package_metadata_result(mod_metadata) is False
    # key expected to be boolean set to wrong type
    mod_metadata = _update_mod_metadata(
        fixture_sample_package_metadata, {"contains_base_objects": 7}
    )
    assert _check_package_metadata_result(mod_metadata) is False
    # __all__ key is not list
    mod_metadata = _update_mod_metadata(fixture_sample_package_metadata, {"__all__": 7})
    assert _check_package_metadata_result(mod_metadata) is False
    # classes key doesn't map to sub-dict with string keys and dict values
    mod_metadata = _update_mod_metadata(
        fixture_sample_package_metadata, {"classes": {"something": 7}}
    )
    assert _check_package_metadata_result(mod_metadata) is False
    # functions key doesn't map to sub-dict with string keys and dict values
    mod_metadata = _update_mod_metadata(
        fixture_sample_package_metadata, {"functions": {"something": 7}}
    )
    assert _check_package_metadata_result(mod_metadata) is False
    # Classes key maps to sub-dict with string keys and dict values, but the
    # dict values don't have correct keys
    mod_metadata = deepcopy(fixture_sample_package_metadata)
    mod_metadata["some_module"]["classes"]["CompositionDummy"].pop("name")
    assert _check_package_metadata_result(mod_metadata) is False
    # function key maps to sub-dict with string keys and dict values, but the
    # dict values don't have correct keys
    mod_metadata = deepcopy(fixture_sample_package_metadata)
    mod_metadata["some_module"]["functions"]["get_package_metadata"].pop("name")
    assert _check_package_metadata_result(mod_metadata) is False


def test_is_non_public_module(mod_names):
    """Test _is_non_public_module correctly identifies non-public modules."""
    for mod in mod_names["public"]:
        assert _is_non_public_module(mod) is False
    for mod in mod_names["non_public"]:
        assert _is_non_public_module(mod) is True


def test_is_non_public_module_raises_error():
    """Test _is_non_public_module raises a ValueError for non-string input."""
    with pytest.raises(ValueError):
        _is_non_public_module(7)


def test_is_ignored_module(mod_names):
    """Test _is_ignored_module correctly identifies modules in ignored sequence."""
    # Test case when no modules are ignored
    for mod in mod_names["public"]:
        assert _is_ignored_module(mod) is False

    # No modules should be flagged as ignored if the ignored modules aren't encountered
    modules_to_ignore = ("a_module_not_encountered",)
    for mod in mod_names["public"]:
        assert _is_ignored_module(mod, modules_to_ignore=modules_to_ignore) is False

    modules_to_ignore = ("_some",)
    for mod in mod_names["non_public"]:
        assert _is_ignored_module(mod, modules_to_ignore=modules_to_ignore) is False

    # When ignored modules are encountered then they should be flagged as True
    modules_to_ignore = ("skbase", "test_mock_package")
    for mod in MOD_NAMES["public"]:
        if "skbase" in mod or "test_mock_package" in mod:
            expected_to_ignore = True
        else:
            expected_to_ignore = False
        assert (
            _is_ignored_module(mod, modules_to_ignore=modules_to_ignore)
            is expected_to_ignore
        )


def test_filter_by_class():
    """Test _filter_by_class correctly identifies classes."""
    # Test case when no class filter is applied (should always return True)
    assert _filter_by_class(CompositionDummy) is True

    # Test case where a single filter is applied
    assert _filter_by_class(Parent, BaseObject) is True
    assert _filter_by_class(NotABaseObject, BaseObject) is False
    assert _filter_by_class(NotABaseObject, CompositionDummy) is False

    # Test case when sequence of classes supplied as filter
    assert _filter_by_class(CompositionDummy, (BaseObject, Parent)) is True
    assert _filter_by_class(CompositionDummy, [NotABaseObject, Parent]) is False


def test_filter_by_tags():
    """Test _filter_by_tags correctly filters classes by their tags or tag values."""
    # Test case when no tag filter is applied (should always return True)
    assert _filter_by_tags(CompositionDummy) is True
    # Even if the class isn't a BaseObject
    assert _filter_by_tags(NotABaseObject) is True

    # Check when tag_filter is a str and present in the class
    assert _filter_by_tags(ClassWithABTrue, tag_filter="A") is True
    # Check when tag_filter is str and not present in the class
    assert _filter_by_tags(Parent, tag_filter="A") is False

    # Test functionality when tag present and object doesn't have tag interface
    assert _filter_by_tags(NotABaseObject, tag_filter="A") is False

    # Test functionality where tag_filter is Iterable of str
    # all tags in iterable are in the class
    assert _filter_by_tags(ClassWithABTrue, ("A", "B")) is True
    # Some tags in iterable are in class and others aren't
    assert _filter_by_tags(ClassWithABTrue, ("A", "B", "C", "D", "E")) is False

    # Test functionality where tag_filter is Dict[str, Any]
    # All keys in dict are in tag_filter and values all match
    assert _filter_by_tags(Parent, {"A": "1", "B": 2}) is True
    # All keys in dict are in tag_filter, but at least 1 value doesn't match
    assert _filter_by_tags(Parent, {"A": 1, "B": 2}) is False
    # At least 1 key in dict is not in tag_filter
    assert _filter_by_tags(Parent, {"E": 1, "B": 2}) is False

    # Iterable tags should be all strings
    with pytest.raises(ValueError, match=r"filter_tags"):
        assert _filter_by_tags(Parent, ("A", "B", 3))

    # Tags that aren't iterable have to be strings
    with pytest.raises(TypeError, match=r"filter_tags"):
        assert _filter_by_tags(Parent, 7.0)

    # Dictionary tags should have string keys
    with pytest.raises(ValueError, match=r"filter_tags"):
        assert _filter_by_tags(Parent, {7: 11})


def test_walk_returns_expected_format(fixture_skbase_root_path):
    """Check walk function returns expected format."""

    def _test_walk_return(p):
        assert (
            isinstance(p, tuple) and len(p) == 3
        ), "_walk should return tuple of length 3"
        assert (
            isinstance(p[0], str)
            and isinstance(p[1], bool)
            and isinstance(p[2], importlib.machinery.FileFinder)
        )

    # Test with string path
    for p in _walk(str(fixture_skbase_root_path)):
        _test_walk_return(p)

    # Test with pathlib.Path
    for p in _walk(fixture_skbase_root_path):
        _test_walk_return(p)


def test_walk_returns_expected_exclude(fixture_test_lookup_mod_path):
    """Check _walk returns expected result when using exclude param."""
    results = list(_walk(str(fixture_test_lookup_mod_path), exclude="tests"))
    assert len(results) == 1
    assert results[0][0] == "_lookup" and results[0][1] is False


@pytest.mark.parametrize("prefix", ["skbase."])
def test_walk_returns_expected_prefix(fixture_skbase_root_path, prefix):
    """Check _walk returns expected result when using prefix param."""
    results = list(_walk(str(fixture_skbase_root_path), prefix=prefix))
    for result in results:
        assert result[0].startswith(prefix)


@pytest.mark.parametrize("suppress_import_stdout", [True, False])
def test_import_module_returns_module(
    fixture_test_lookup_mod_path, suppress_import_stdout
):
    """Test that _import_module returns a module type."""
    # Import module based on name case
    imported_mod = _import_module(
        "pytest", suppress_import_stdout=suppress_import_stdout
    )
    assert isinstance(imported_mod, ModuleType)

    # Import module based on SourceFileLoader for a file path
    # First specify path to _lookup.py relative to this file
    path = str(fixture_test_lookup_mod_path / "_lookup.py")
    loader = importlib.machinery.SourceFileLoader("_lookup", path)
    imported_mod = _import_module(loader, suppress_import_stdout=suppress_import_stdout)
    assert isinstance(imported_mod, ModuleType)


def test_import_module_raises_error_invalid_input():
    """Test that _import_module raises an error with invalid input."""
    match = " ".join(
        [
            "`module` should be string module name or instance of",
            "importlib.machinery.SourceFileLoader.",
        ]
    )
    with pytest.raises(ValueError, match=match):
        _import_module(7)


def test_determine_module_path_output_types(
    fixture_skbase_root_path, fixture_test_lookup_mod_path
):
    """Test _determine_module_path returns expected output types."""

    def _check_determine_module_path(result):
        assert isinstance(result[0], ModuleType)
        assert isinstance(result[1], str)
        assert isinstance(result[2], importlib.machinery.SourceFileLoader)

    # Test with package_name and path
    result = _determine_module_path("skbase", path=fixture_skbase_root_path)
    _check_determine_module_path(result)
    # Test with package_name
    result = _determine_module_path("pytest")
    _check_determine_module_path(result)

    path = str(fixture_test_lookup_mod_path / "_lookup.py")
    # Test with package_name and path
    result = _determine_module_path("skbase.lookup._lookup", path=path)
    _check_determine_module_path(result)


def test_determine_module_path_raises_error_invalid_input(fixture_skbase_root_path):
    """Test that _import_module raises an error with invalid input."""
    with pytest.raises(ValueError):
        _determine_module_path(7, path=fixture_skbase_root_path)

    with pytest.raises(ValueError):
        _determine_module_path(fixture_skbase_root_path, path=fixture_skbase_root_path)

    with pytest.raises(ValueError):
        _determine_module_path("skbase", path=7)


@pytest.mark.parametrize("recursive", [True, False])
@pytest.mark.parametrize("exclude_non_public_items", [True, False])
@pytest.mark.parametrize("exclude_non_public_modules", [True, False])
@pytest.mark.parametrize("modules_to_ignore", ["tests", ("testing", "tests"), None])
@pytest.mark.parametrize(
    "package_base_classes", [BaseObject, (BaseObject, BaseEstimator), None]
)
@pytest.mark.parametrize("suppress_import_stdout", [True, False])
def test_get_package_metadata_returns_expected_types(
    recursive,
    exclude_non_public_items,
    exclude_non_public_modules,
    modules_to_ignore,
    package_base_classes,
    suppress_import_stdout,
):
    """Test get_package_metadata returns expected output types."""
    results = get_package_metadata(
        "skbase",
        recursive=recursive,
        exclude_non_public_items=exclude_non_public_items,
        exclude_non_public_modules=exclude_non_public_modules,
        modules_to_ignore=modules_to_ignore,
        package_base_classes=package_base_classes,
        classes_to_exclude=TagAliaserMixin,
        suppress_import_stdout=suppress_import_stdout,
    )
    # Verify we return dict with str keys
    assert _check_package_metadata_result(results) is True

    # Verify correct behavior of modules_to_ignore
    no_ignored_module_returned = [
        not _is_ignored_module(k, modules_to_ignore=modules_to_ignore) for k in results
    ]

    assert all(no_ignored_module_returned)

    klass_metadata = [
        klass_metadata
        for module in results.values()
        for klass_metadata in module["classes"].values()
    ]
    # Verify correct behavior of exclude_non_public_items
    if exclude_non_public_items:
        expected_nonpublic_classes_returned = [
            not k["name"].startswith("_") for k in klass_metadata
        ]
        assert all(expected_nonpublic_classes_returned)

        expected_nonpublic_funcs_returned = [
            not func_metadata["name"].startswith("_")
            for module in results.values()
            for func_metadata in module["functions"].values()
        ]
        assert all(expected_nonpublic_funcs_returned)

    # Verify correct behavior of exclude_non_public_modules
    if exclude_non_public_modules:
        expected_nonpublic_modules_returned = [
            not _is_non_public_module(k) for k in results
        ]
        assert all(expected_nonpublic_modules_returned)

    if package_base_classes is not None:
        if isinstance(package_base_classes, type):
            package_base_classes = (package_base_classes,)
        expected_is_base_class_returned = [
            (
                k["klass"] in package_base_classes
                if k["is_base_class"]
                else k["klass"] not in package_base_classes
            )
            for k in klass_metadata
        ]
        assert all(expected_is_base_class_returned)


# This is separate from other get_package_metadata tests b/c right now
# tests on broader skbase package must exclude TagAliaserMixin or they will error
# Once TagAliaserMixin is removed or get_class_tags made fully compliant, this
# will be combined above
@pytest.mark.parametrize(
    "classes_to_exclude",
    [None, CompositionDummy, (CompositionDummy, NotABaseObject)],
)
def test_get_package_metadata_classes_to_exclude(classes_to_exclude):
    """Test get_package_metadata classes_to_exclude param works as expected."""
    results = get_package_metadata(
        "skbase.tests",
        recursive=True,
        exclude_non_public_items=True,
        exclude_non_public_modules=True,
        modules_to_ignore=None,
        package_base_classes=None,
        classes_to_exclude=classes_to_exclude,
        suppress_import_stdout=True,
    )
    # Verify we return dict with str keys
    assert _check_package_metadata_result(results) is True
    if classes_to_exclude is not None:
        if isinstance(classes_to_exclude, type):
            excluded_classes = (classes_to_exclude,)
        else:
            excluded_classes = classes_to_exclude
        # Verify classes_to_exclude works as expected
        classes_excluded_as_expected = [
            klass_metadata["klass"] not in excluded_classes
            for module in results.values()
            for klass_metadata in module["classes"].values()
        ]
        assert all(classes_excluded_as_expected)


@pytest.mark.parametrize(
    "class_filter", [None, BaseEstimator, (BaseObject, BaseEstimator)]
)
def test_get_package_metadata_class_filter(class_filter):
    """Test get_package_metadata filters by class as expected."""
    # Results applying filter
    results = get_package_metadata(
        "skbase",
        modules_to_ignore="skbase",
        class_filter=class_filter,
        classes_to_exclude=TagAliaserMixin,
    )
    filtered_classes = [
        klass_metadata["klass"]
        for module in results.values()
        for klass_metadata in module["classes"].values()
    ]

    # Results without filter
    unfiltered_results = get_package_metadata(
        "skbase",
        modules_to_ignore="skbase",
        classes_to_exclude=TagAliaserMixin,
    )
    unfiltered_classes = [
        klass_metadata["klass"]
        for module in unfiltered_results.values()
        for klass_metadata in module["classes"].values()
    ]

    # Verify filtered results have right output type
    assert _check_package_metadata_result(results) is True

    # Now verify class filter is being applied correctly
    if class_filter is None:
        assert len(unfiltered_classes) == len(filtered_classes)
        assert unfiltered_classes == filtered_classes
    else:
        assert len(unfiltered_classes) > len(filtered_classes)
        classes_subclass_class_filter = [
            issubclass(klass, class_filter) for klass in filtered_classes
        ]
        assert all(classes_subclass_class_filter)


@pytest.mark.parametrize("tag_filter", [None, "A", ("A", "B"), {"A": "1", "B": 2}])
def test_get_package_metadata_tag_filter(tag_filter):
    """Test get_package_metadata filters by tags as expected."""
    results = get_package_metadata(
        "skbase",
        exclude_non_public_modules=False,
        modules_to_ignore="skbase",
        tag_filter=tag_filter,
        classes_to_exclude=TagAliaserMixin,
    )
    filtered_classes = [
        klass_metadata["klass"]
        for module in results.values()
        for klass_metadata in module["classes"].values()
    ]

    # Unfiltered results
    unfiltered_results = get_package_metadata(
        "skbase",
        exclude_non_public_modules=False,
        modules_to_ignore="skbase",
        classes_to_exclude=TagAliaserMixin,
    )
    unfiltered_classes = [
        klass_metadata["klass"]
        for module in unfiltered_results.values()
        for klass_metadata in module["classes"].values()
    ]

    # Verify we return dict with str keys
    assert _check_package_metadata_result(results) is True

    # Verify tag filter is being applied correctly, which implies
    # When the filter is None the result is the same size
    # Otherwise, with the filters used in the test, fewer classes should
    # be returned
    if tag_filter is None:
        assert len(unfiltered_classes) == len(filtered_classes)
        assert unfiltered_classes == filtered_classes
    else:
        assert len(unfiltered_classes) > len(filtered_classes)


@pytest.mark.parametrize("exclude_non_public_modules", [True, False])
@pytest.mark.parametrize("exclude_non_public_items", [True, False])
def test_get_package_metadata_returns_expected_results(
    exclude_non_public_modules, exclude_non_public_items
):
    """Test that get_package_metadata_returns expected results using skbase."""
    results = get_package_metadata(
        "skbase",
        exclude_non_public_items=exclude_non_public_items,
        exclude_non_public_modules=exclude_non_public_modules,
        package_base_classes=SKBASE_BASE_CLASSES,
        modules_to_ignore="tests",
        classes_to_exclude=TagAliaserMixin,
        suppress_import_stdout=False,
    )
    public_modules_excluding_tests = [
        module
        for module in SKBASE_PUBLIC_MODULES
        if not _is_ignored_module(module, modules_to_ignore="tests")
    ]
    modules_excluding_tests = [
        module
        for module in SKBASE_MODULES
        if not _is_ignored_module(module, modules_to_ignore="tests")
    ]
    if exclude_non_public_modules:
        assert tuple(results.keys()) == tuple(public_modules_excluding_tests)
    else:
        assert tuple(results.keys()) == tuple(modules_excluding_tests)

    for module in results:
        if exclude_non_public_items:
            module_funcs = SKBASE_PUBLIC_FUNCTIONS_BY_MODULE.get(module, ())
            module_classes = SKBASE_PUBLIC_CLASSES_BY_MODULE.get(module, ())
            which_str = "public"
            fun_str = "SKBASE_PUBLIC_FUNCTIONS_BY_MODULE"
            cls_str = "SKBASE_PUBLIC_CLASSES_BY_MODULE"
        else:
            module_funcs = SKBASE_FUNCTIONS_BY_MODULE.get(module, ())
            module_classes = SKBASE_CLASSES_BY_MODULE.get(module, ())
            which_str = "all"
            fun_str = "SKBASE_FUNCTIONS_BY_MODULE"
            cls_str = "SKBASE_CLASSES_BY_MODULE"

        # Verify expected functions are returned
        retrieved_funcs = set(results[module]["functions"].keys())
        expected_funcs = set(module_funcs)

        if retrieved_funcs != expected_funcs:
            msg = (
                "When using get_package_metadata utility, retrieved objects "
                f"for {which_str} functions in module {module} do not match expected. "
                f"Expected: {expected_funcs}; "
                f"retrieved: {retrieved_funcs}. "
                f"Expected functions are stored in {fun_str}, in test_lookup."
            )
            raise AssertionError(msg)

        # Verify expected classes are returned
        retrieved_cls = set(results[module]["classes"].keys())
        expected_cls = set(module_classes)

        if retrieved_cls != expected_cls:
            msg = (
                "When using get_package_metadata utility, retrieved objects "
                f"for {which_str} classes in module {module} do not match expected. "
                f"Expected: {expected_cls}; "
                f"retrieved: {retrieved_cls}. "
                f"Expected functions are stored in {cls_str}, in test_lookup."
            )
            raise AssertionError(msg)

        # Verify class metadata attributes correct
        for klass, klass_metadata in results[module]["classes"].items():
            if klass_metadata["klass"] in SKBASE_BASE_CLASSES:
                assert (
                    klass_metadata["is_base_class"] is True
                ), f"{klass} should be base class."
            else:
                assert (
                    klass_metadata["is_base_class"] is False
                ), f"{klass} should not be base class."

            if issubclass(klass_metadata["klass"], BaseObject):
                assert klass_metadata["is_base_object"] is True
            else:
                assert klass_metadata["is_base_object"] is False

            if (
                issubclass(klass_metadata["klass"], SKBASE_BASE_CLASSES)
                and klass_metadata["klass"] not in SKBASE_BASE_CLASSES
            ):
                assert klass_metadata["is_concrete_implementation"] is True
            else:
                assert klass_metadata["is_concrete_implementation"] is False


def test_get_return_tags():
    """Test _get_return_tags returns expected."""

    def _test_get_return_tags_output(results, num_requested_tags):
        return isinstance(results, tuple) and len(results) == num_requested_tags

    # Verify return with tags that exist
    tags = Parent.get_class_tags()
    tag_names = [*tags.keys()]
    results = _get_return_tags(Parent, tag_names)
    assert (
        _test_get_return_tags_output(results, len(tag_names))
        and tuple(tags.values()) == results
    )

    # Verify results when some exist and some don't exist
    tag_names += ["a_tag_that_does_not_exist"]
    results = _get_return_tags(Parent, tag_names)
    assert _test_get_return_tags_output(results, len(tag_names))

    # Verify return when all tags don't exist
    tag_names = ["a_tag_that_does_not_exist"]
    results = _get_return_tags(Parent, tag_names)
    assert _test_get_return_tags_output(results, len(tag_names)) and results[0] is None


@pytest.mark.parametrize("as_dataframe", [True, False])
@pytest.mark.parametrize("return_names", [True, False])
@pytest.mark.parametrize("return_tags", [None, "A", ["A", "a_non_existent_tag"]])
@pytest.mark.parametrize("modules_to_ignore", ["tests", ("testing", "lookup"), None])
@pytest.mark.parametrize("exclude_objects", [None, "Child", ["CompositionDummy"]])
@pytest.mark.parametrize("suppress_import_stdout", [True, False])
def test_all_objects_returns_expected_types(
    as_dataframe,
    return_names,
    return_tags,
    modules_to_ignore,
    exclude_objects,
    suppress_import_stdout,
):
    """Test that all_objects return argument has correct type.

    Also tested: sys.stdout is unchanged after function call, see bug #327.
    """
    # we will check later that sys.stdout is unchanged
    initial_stdout = sys.stdout

    # call all_objects
    objs = all_objects(
        package_name="skbase",
        exclude_objects=exclude_objects,
        return_names=return_names,
        as_dataframe=as_dataframe,
        return_tags=return_tags,
        modules_to_ignore=modules_to_ignore,
        suppress_import_stdout=suppress_import_stdout,
    )

    # verify sys.stdout is unchanged
    assert sys.stdout == initial_stdout

    # verify output has expected types
    if isinstance(modules_to_ignore, str):
        modules_to_ignore = (modules_to_ignore,)
    if (
        modules_to_ignore is not None
        and "tests" in modules_to_ignore
        # and "mock_package" in modules_to_ignore
    ):
        assert (
            len(objs) == 0
        ), "Search of `skbase` should only return objects from tests module."
    else:
        # We expect at least one object to be returned so we verify output type/format
        _check_all_object_output_types(
            objs,
            as_dataframe=as_dataframe,
            return_names=return_names,
            return_tags=return_tags,
        )


@pytest.mark.parametrize(
    "exclude_objects", [None, "Parent", ["Child", "CompositionDummy"]]
)
def test_all_objects_returns_expected_output(exclude_objects):
    """Test that all_objects return argument has correct output for skbase."""
    objs = all_objects(
        package_name="skbase.tests.mock_package",
        exclude_objects=exclude_objects,
        return_names=True,
        as_dataframe=True,
        modules_to_ignore="conftest",
        suppress_import_stdout=True,
    )
    klasses = objs["object"].tolist()
    test_classes = [
        k
        for k in MOCK_PACKAGE_OBJECTS
        if issubclass(k, BaseObject) and not k.__name__.startswith("_")
    ]
    if exclude_objects is not None:
        if isinstance(exclude_objects, str):
            exclude_objects = (exclude_objects,)
        # Exclude classes from MOCK_PACKAGE_OBJECTS
        test_classes = [k for k in test_classes if k.__name__ not in exclude_objects]

    msg = f"{klasses} should match test classes {test_classes}."
    assert set(klasses) == set(test_classes), msg


@pytest.mark.parametrize("class_filter", [None, Parent, [Parent, BaseEstimator]])
def test_all_objects_class_filter(class_filter):
    """Test all_objects filters by class type as expected."""
    # Results applying filter
    objs = all_objects(
        package_name="skbase",
        return_names=True,
        as_dataframe=True,
        return_tags=None,
        object_types=class_filter,
    )
    filtered_classes = objs.iloc[:, 1].tolist()
    # Verify filtered results have right output type
    _check_all_object_output_types(
        objs, as_dataframe=True, return_names=True, return_tags=None
    )

    # Results without filter
    objs = all_objects(
        package_name="skbase",
        return_names=True,
        as_dataframe=True,
        return_tags=None,
    )
    unfiltered_classes = objs.iloc[:, 1].tolist()

    # Now verify class filter is being applied correctly
    if class_filter is None:
        assert len(unfiltered_classes) == len(filtered_classes)
        assert unfiltered_classes == filtered_classes
    else:
        if not isinstance(class_filter, type):
            class_filter = tuple(class_filter)
        assert len(unfiltered_classes) > len(filtered_classes)
        classes_subclass_class_filter = [
            issubclass(klass, class_filter) for klass in filtered_classes
        ]
        assert all(classes_subclass_class_filter)


@pytest.mark.parametrize("tag_filter", [None, "A", ("A", "B"), {"A": "1", "B": 2}])
def test_all_object_tag_filter(tag_filter):
    """Test all_objects filters by tag as expected."""
    # Results applying filter
    objs = all_objects(
        package_name="skbase",
        return_names=True,
        as_dataframe=True,
        return_tags=None,
        filter_tags=tag_filter,
    )
    filtered_classes = objs.iloc[:, 1].tolist()
    # Verify filtered results have right output type
    _check_all_object_output_types(
        objs, as_dataframe=True, return_names=True, return_tags=None
    )

    # Results without filter
    objs = all_objects(
        package_name="skbase",
        return_names=True,
        as_dataframe=True,
        return_tags=None,
    )
    unfiltered_classes = objs.iloc[:, 1].tolist()

    # Verify tag filter is being applied correctly, which implies
    # When the filter is None the result is the same size
    # Otherwise, with the filters used in the test, fewer classes should
    # be returned
    if tag_filter is None:
        assert len(unfiltered_classes) == len(filtered_classes)
        assert unfiltered_classes == filtered_classes
    else:
        assert len(unfiltered_classes) > len(filtered_classes)


def test_all_object_tag_filter_regex():
    """Test all_objects filters by tag as expected, when using regex."""
    import re

    # search for class where "A" has at least one 1, and "C" has "23" in the tag value
    # this sohuld find Parent but not Child
    filter_tags = {"A": re.compile(r"^(?=.*1).*$"), "C": re.compile(r".+23.+")}

    # Results applying filter
    objs = all_objects(
        package_name="skbase",
        return_names=True,
        as_dataframe=True,
        return_tags=None,
        filter_tags=filter_tags,
    )
    filtered_classes = objs.iloc[:, 1].tolist()
    # Verify filtered results have right output type
    _check_all_object_output_types(
        objs, as_dataframe=True, return_names=True, return_tags=None
    )

    # Results without filter
    objs = all_objects(
        package_name="skbase",
        return_names=True,
        as_dataframe=True,
        return_tags=None,
    )
    unfiltered_classes = objs.iloc[:, 1].tolist()

    # as stated above, we should find only Parent (and not Child)
    assert len(unfiltered_classes) > len(filtered_classes)
    names = [kls.__name__ for kls in filtered_classes]
    assert "Parent" in names


@pytest.mark.parametrize("class_lookup", [{"base_object": BaseObject}])
@pytest.mark.parametrize("class_filter", [None, "base_object"])
def test_all_object_class_lookup(class_lookup, class_filter):
    """Test all_objects class_lookup parameter works as expected.."""
    # Results applying filter
    objs = all_objects(
        package_name="skbase",
        return_names=True,
        as_dataframe=True,
        return_tags=None,
        object_types=class_filter,
        class_lookup=class_lookup,
    )
    # filtered_classes = objs.iloc[:, 1].tolist()
    # Verify filtered results have right output type
    _check_all_object_output_types(
        objs, as_dataframe=True, return_names=True, return_tags=None
    )


@pytest.mark.parametrize("class_lookup", [None, {"base_object": BaseObject}])
@pytest.mark.parametrize("class_filter", ["invalid_alias", 7])
def test_all_object_class_lookup_invalid_object_types_raises(
    class_lookup, class_filter
):
    """Test all_objects use of object filtering raises errors as expected."""
    # Results applying filter
    with pytest.raises(ValueError):
        all_objects(
            package_name="skbase",
            return_names=True,
            as_dataframe=True,
            return_tags=None,
            object_types=class_filter,
            class_lookup=class_lookup,
        )
