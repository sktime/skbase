# -*- coding: utf-8 -*-
"""Tests for _check_soft_dependencies utility."""
from unittest.mock import patch

import pytest
from packaging.requirements import InvalidRequirement

from skbase.utils.dependencies import (
    _check_python_version,
    _check_soft_dependencies,
)


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


def test_check_soft_dependencies_nested():
    """Test check_soft_dependencies with ."""
    ALWAYS_INSTALLED = "pytest"  # noqa: N806
    ALWAYS_INSTALLED2 = "numpy"  # noqa: N806
    ALWAYS_INSTALLED_W_V = "pytest>=0.5.0"  # noqa: N806
    ALWAYS_INSTALLED_W_V2 = "numpy>=0.1.0"  # noqa: N806
    NEVER_INSTALLED = "nonexistent__package_foo_bar"  # noqa: N806
    NEVER_INSTALLED_W_V = "pytest<0.1.0"  # noqa: N806

    # Test that the function does not raise an error when all dependencies are installed
    _check_soft_dependencies(ALWAYS_INSTALLED)
    _check_soft_dependencies(ALWAYS_INSTALLED, ALWAYS_INSTALLED2)
    _check_soft_dependencies(ALWAYS_INSTALLED_W_V)
    _check_soft_dependencies(ALWAYS_INSTALLED_W_V, ALWAYS_INSTALLED_W_V2)
    _check_soft_dependencies(ALWAYS_INSTALLED, ALWAYS_INSTALLED2, ALWAYS_INSTALLED_W_V2)
    _check_soft_dependencies([ALWAYS_INSTALLED, ALWAYS_INSTALLED2])

    # Test that error is raised when a dependency is not installed
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies(NEVER_INSTALLED)
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies(NEVER_INSTALLED, ALWAYS_INSTALLED)
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies([ALWAYS_INSTALLED, NEVER_INSTALLED])
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies(ALWAYS_INSTALLED, NEVER_INSTALLED_W_V)
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies([ALWAYS_INSTALLED, NEVER_INSTALLED_W_V])

    # disjunction cases, "or" - positive cases
    _check_soft_dependencies([[ALWAYS_INSTALLED, NEVER_INSTALLED]])
    _check_soft_dependencies(
        [
            [ALWAYS_INSTALLED, NEVER_INSTALLED],
            [ALWAYS_INSTALLED_W_V, NEVER_INSTALLED_W_V],
            ALWAYS_INSTALLED2,
        ]
    )

    # disjunction cases, "or" - negative cases
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies([[NEVER_INSTALLED, NEVER_INSTALLED_W_V]])
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies(
            [
                [NEVER_INSTALLED, NEVER_INSTALLED_W_V],
                [ALWAYS_INSTALLED, NEVER_INSTALLED],
                ALWAYS_INSTALLED2,
            ]
        )
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies(
            [
                ALWAYS_INSTALLED2,
                [ALWAYS_INSTALLED, NEVER_INSTALLED],
                NEVER_INSTALLED_W_V,
            ]
        )
    with pytest.raises(ModuleNotFoundError):
        _check_soft_dependencies(
            [
                [ALWAYS_INSTALLED, ALWAYS_INSTALLED2],
                NEVER_INSTALLED,
                ALWAYS_INSTALLED2,
            ]
        )


@patch("skbase.utils.dependencies._dependencies.sys")
@pytest.mark.parametrize(
    "mock_release_version, prereleases, expect_exception",
    [
        (True, True, False),
        (True, False, True),
        (False, False, False),
        (False, True, False),
    ],
)
def test_check_python_version(
    mock_sys, mock_release_version, prereleases, expect_exception
):
    from skbase.base import BaseObject

    if mock_release_version:
        mock_sys.version = "3.8.1rc"
    else:
        mock_sys.version = "3.8.1"

    class DummyObjectClass(BaseObject):
        _tags = {
            "python_version": ">=3.7.1",  # PEP 440 version specifier, e.g., ">=3.7"
            "python_dependencies": None,  # PEP 440 dependency strs, e.g., "pandas>=1.0"
            "env_marker": None,  # PEP 508 environment marker, e.g., "os_name=='posix'"
        }
        """Define dummy class to test set_tags."""

    dummy_object_instance = DummyObjectClass()

    try:
        _check_python_version(dummy_object_instance, prereleases=prereleases)
    except ModuleNotFoundError as exception:
        expected_msg = (
            f"{type(dummy_object_instance).__name__} requires python version "
            f"to be {dummy_object_instance.get_tags()['python_version']}, "
            f"but system python version is {mock_sys.version}. "
            "This is due to the release candidate status of your system Python."
        )

        if not expect_exception or exception.msg != expected_msg:
            # Throw Error since exception is not expected or has not the correct message
            raise AssertionError(
                "ModuleNotFoundError should be NOT raised by:",
                f"\n\t - mock_release_version: {mock_release_version},",
                f"\n\t - prereleases: {prereleases},",
                f"\nERROR MESSAGE: {exception.msg}",
            ) from exception
