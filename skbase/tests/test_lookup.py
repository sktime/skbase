"""Tests for skbase.lookup utilities."""


def test_all_objects_filter_tags_returns_results(tmp_path, monkeypatch):


    import importlib

    from skbase.base import BaseObject  # noqa: F401
    from skbase.lookup import all_objects

    root = tmp_path / "pkg"
    root.mkdir()

    # create __init__.py
    (root / "__init__.py").write_text(
        "from .module import MyObject\n__all__ = ['MyObject']\n"
    )

    # create module.py
    (root / "module.py").write_text(
        "from skbase.base import BaseObject\n"
        "class MyObject(BaseObject):\n"
        "    _tags = {'my_tag': True}\n"
    )

    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()

    objs = all_objects(package_name="pkg", filter_tags="my_tag")
    assert len(objs) > 0
