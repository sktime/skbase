# -*- coding: utf-8 -*-
"""Tests for lookup utilities handling classes defined with metaclasses."""

from typing import List, Tuple

from skbase.lookup import all_objects, get_package_metadata
from skbase.tests.metaclass_objects import MetaExample, MetaSubclass
from skbase.utils.dependencies._import import CommonMagicMeta, MagicAttribute

__author__: List[str] = ["SimonBlanke"]


def _metaclass_ignore_modules() -> Tuple[str, ...]:
    """Return modules we ignore to keep imports light in tests."""
    return (
        "test_base",
        "test_baseestimator",
        "test_meta",
        "test_exceptions",
        "test_tagaliaser",
        "mock_package",
        "conftest",
        "test_lookup_metaclasses",
    )


def test_all_objects_discovers_metaclass_classes():
    """Classes defined with metaclasses should be returned by all_objects."""
    results = all_objects(
        package_name="skbase.tests",
        object_types=object,
        modules_to_ignore=_metaclass_ignore_modules(),
        suppress_import_stdout=True,
    )
    objects = dict(results)

    assert objects["MetaExample"] is MetaExample
    assert objects["MetaSubclass"] is MetaSubclass
    assert objects["CommonMagicMeta"] is CommonMagicMeta


def test_get_package_metadata_tracks_metaclass_classes():
    """get_package_metadata should capture metaclass-based classes without mocking."""
    metadata = get_package_metadata(
        package_name="skbase.utils.dependencies._import",
        modules_to_ignore=(),
        suppress_import_stdout=True,
    )
    module_key = "skbase.utils.dependencies._import"
    module_info = metadata[module_key]
    classes = module_info["classes"]

    assert "MagicAttribute" in classes
    assert "CommonMagicMeta" in classes

    magic_attribute_info = classes["MagicAttribute"]
    common_magic_meta_info = classes["CommonMagicMeta"]

    assert magic_attribute_info["klass"] is MagicAttribute
    assert common_magic_meta_info["klass"] is CommonMagicMeta
    assert magic_attribute_info["module_name"] == module_key
    assert common_magic_meta_info["module_name"] == module_key
