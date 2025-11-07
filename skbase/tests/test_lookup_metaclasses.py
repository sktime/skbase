# -*- coding: utf-8 -*-
"""Tests for lookup helpers handling classes defined with metaclasses."""

import importlib
import inspect
from typing import List

from skbase.lookup import get_package_metadata
from skbase.lookup._lookup import _get_members_uw
from skbase.utils.dependencies._import import CommonMagicMeta, MagicAttribute

__author__: List[str] = ["SimonBlanke"]


def test_get_members_uw_discovers_metaclass_classes():
    """_get_members_uw should retain classes even when unwrapping metaclass objects."""
    module = importlib.import_module("skbase.utils.dependencies._import")
    members = dict(_get_members_uw(module, inspect.isclass))

    assert members["MagicAttribute"] is MagicAttribute
    assert members["CommonMagicMeta"] is CommonMagicMeta


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
