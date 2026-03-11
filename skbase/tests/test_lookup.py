"""Tests for skbase.lookup utilities."""

import importlib
import sys

from skbase.lookup import all_objects


def test_all_objects_returns_class_name_for_alias(tmp_path, monkeypatch):
    """all_objects should report the underlying class name, not an alias."""
    pkg_name = "pkg_alias_case"
    root = tmp_path / pkg_name
    root.mkdir()

    # create a tmp module to test all_objects behaviour
    (root / "__init__.py").write_text(
        "from .module import AliasName\n" "__all__ = ['AliasName']\n"
    )
    (root / "module.py").write_text(
        "from skbase.base import BaseObject\n\n"
        "class ActualName(BaseObject):\n"
        "    pass\n\n"
        "AliasName = ActualName\n"
        "__all__ = ['AliasName']\n"
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()

    objs = all_objects(package_name=pkg_name, path=str(root))
    assert len(objs) == 1
    name, klass = objs[0]
    assert name == klass.__name__ == "ActualName"

    sys.modules.pop(f"{pkg_name}.module", None)
    sys.modules.pop(pkg_name, None)


# -- helpers for exclude_tags tests ------------------------------------------

_TAGGED_PKG_SRC_INIT = (
    "from .module import ObjA, ObjB, ObjC\n" "__all__ = ['ObjA', 'ObjB', 'ObjC']\n"
)

_TAGGED_PKG_SRC_MODULE = (
    "from skbase.base import BaseObject\n\n"
    "class ObjA(BaseObject):\n"
    "    _tags = {'deprecated': True, 'capability:missing_values': True}\n\n"
    "class ObjB(BaseObject):\n"
    "    _tags = {'deprecated': False, 'capability:missing_values': True}\n\n"
    "class ObjC(BaseObject):\n"
    "    _tags = {'deprecated': False, 'capability:missing_values': False}\n"
)


def _make_tagged_pkg(tmp_path, monkeypatch, pkg_name="tagged_pkg"):
    """Create a tiny temp package with tagged BaseObject subclasses."""
    root = tmp_path / pkg_name
    root.mkdir()
    (root / "__init__.py").write_text(_TAGGED_PKG_SRC_INIT)
    (root / "module.py").write_text(_TAGGED_PKG_SRC_MODULE)
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    return root, pkg_name


def _cleanup_tagged_pkg(pkg_name="tagged_pkg"):
    """Remove the temp package from sys.modules."""
    for key in list(sys.modules):
        if key == pkg_name or key.startswith(f"{pkg_name}."):
            sys.modules.pop(key, None)


# -- exclude_tags tests ------------------------------------------------------


def test_exclude_tags_none_is_noop(tmp_path, monkeypatch):
    """exclude_tags=None should return all objects (backwards compatible)."""
    root, pkg_name = _make_tagged_pkg(tmp_path, monkeypatch)
    try:
        result = all_objects(package_name=pkg_name, path=str(root), exclude_tags=None)
        names = [n for n, _ in result]
        assert "ObjA" in names
        assert "ObjB" in names
        assert "ObjC" in names
    finally:
        _cleanup_tagged_pkg(pkg_name)


def test_exclude_tags_empty_dict_is_noop(tmp_path, monkeypatch):
    """exclude_tags={} should return all objects."""
    root, pkg_name = _make_tagged_pkg(tmp_path, monkeypatch)
    try:
        result_all = all_objects(package_name=pkg_name, path=str(root))
        result_empty = all_objects(
            package_name=pkg_name,
            path=str(root),
            exclude_tags={},
        )
        assert len(result_all) == len(result_empty)
    finally:
        _cleanup_tagged_pkg(pkg_name)


def test_exclude_tags_excludes_matching(tmp_path, monkeypatch):
    """exclude_tags should remove objects whose tags match."""
    root, pkg_name = _make_tagged_pkg(tmp_path, monkeypatch)
    try:
        result = all_objects(
            package_name=pkg_name,
            path=str(root),
            exclude_tags={"deprecated": True},
        )
        names = [n for n, _ in result]
        assert "ObjA" not in names, "ObjA is deprecated and should be excluded"
        assert "ObjB" in names
        assert "ObjC" in names
    finally:
        _cleanup_tagged_pkg(pkg_name)


def test_exclude_tags_combined_with_filter_tags(tmp_path, monkeypatch):
    """filter_tags + exclude_tags should filter first, then exclude."""
    root, pkg_name = _make_tagged_pkg(tmp_path, monkeypatch)
    try:
        result = all_objects(
            package_name=pkg_name,
            path=str(root),
            filter_tags={"capability:missing_values": True},
            exclude_tags={"deprecated": True},
        )
        names = [n for n, _ in result]
        # ObjA has missing_values=True but deprecated=True -> excluded
        assert "ObjA" not in names
        # ObjB has missing_values=True and deprecated=False -> included
        assert "ObjB" in names
        # ObjC has missing_values=False -> filtered out by filter_tags
        assert "ObjC" not in names
    finally:
        _cleanup_tagged_pkg(pkg_name)


def test_exclude_tags_multiple_conditions(tmp_path, monkeypatch):
    """exclude_tags with multiple keys should exclude on conjunction."""
    root, pkg_name = _make_tagged_pkg(tmp_path, monkeypatch)
    try:
        # Exclude objects where BOTH deprecated=True AND missing_values=True
        # Only ObjA matches both -> excluded
        result = all_objects(
            package_name=pkg_name,
            path=str(root),
            exclude_tags={
                "deprecated": True,
                "capability:missing_values": True,
            },
        )
        names = [n for n, _ in result]
        assert "ObjA" not in names
        assert "ObjB" in names
        assert "ObjC" in names
    finally:
        _cleanup_tagged_pkg(pkg_name)
