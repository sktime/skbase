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


def test_all_objects_filter_tags_not_empty():
    from skbase.base import all_objects

    objs = all_objects()
    assert len(objs) > 0

    first_obj = objs[0][1]
    tags = first_obj.get_class_tags()

    tag_name, tag_value = next(iter(tags.items()))

    filtered = all_objects(filter_tags={tag_name: tag_value})

    assert len(filtered) > 0
