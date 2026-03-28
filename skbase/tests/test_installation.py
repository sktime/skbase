"""Tests for skbase package installation and compliance."""

import os

import skbase


def test_py_typed_marker_exists():
    """Test that py.typed marker file exists for PEP 561 compliance."""
    package_dir = os.path.dirname(skbase.__file__)
    py_typed_path = os.path.join(package_dir, "py.typed")
    assert os.path.isfile(py_typed_path), (
        "py.typed marker file is missing from skbase package. "
        "This file is required for PEP 561 compliance so that "
        "mypy and pyright can use skbase's type annotations."
    )
