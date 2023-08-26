# -*- coding: utf-8 -*-
"""Tests for _check_soft_dependencies utility."""
import pytest
from packaging.requirements import InvalidRequirement

from skbase.utils.dependencies._dependencies import _check_soft_dependencies


def test_check_soft_deps():
    """Test package availability against pyproject of skbase."""
    # test various admissible input types, positives
    assert _check_soft_dependencies("pytest")
    assert _check_soft_dependencies("pytest", "numpy")
    assert _check_soft_dependencies("pytest", "numpy")
    assert _check_soft_dependencies(["pytest", "numpy"])
    assert _check_soft_dependencies(("pytest", "numpy"))

    # test various admissible input types, negatives
    assert not _check_soft_dependencies("humpty", severity="none")
    assert not _check_soft_dependencies("numpy", "dumpty", severity="none")
    assert not _check_soft_dependencies("humpty", "numpy", severity="none")
    assert not _check_soft_dependencies(["humpty", "humpty"], severity="none")
    assert not _check_soft_dependencies(("humpty", "dumpty"), severity="none")

    # test error raise on error severity
    with pytest.raises(ModuleNotFoundError):
        assert _check_soft_dependencies("humpty", severity="error")
    with pytest.raises(ModuleNotFoundError):
        assert _check_soft_dependencies("numpy", "dumpty", severity="error")

    # test warning on warning severity
    with pytest.warns():
        assert not _check_soft_dependencies("humpty", severity="warning")
    with pytest.warns():
        assert not _check_soft_dependencies("numpy", "dumpty", severity="warning")

    # test valid PEP 440 specifier strings
    assert _check_soft_dependencies("pytest>0.0.1")
    assert _check_soft_dependencies("pytest>=0.0.1", "numpy!=0.1.0")
    assert not _check_soft_dependencies(("pytest", "numpy<0.1.0"), severity="none")
    assert _check_soft_dependencies(["pytest", "numpy>0.1.0"], severity="none")

    # test error on invalid PEP 440 specifier string
    with pytest.raises(InvalidRequirement):
        assert _check_soft_dependencies("pytest!!!!>>>0.0.1")
    with pytest.raises(InvalidRequirement):
        assert _check_soft_dependencies(
            ("pytest", "!!numpy<~><>0.1.0"), severity="none"
        )
