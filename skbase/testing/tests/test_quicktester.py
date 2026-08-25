# -*- coding: utf-8 -*-
"""Regression tests for QuickTester input checks and output muting."""

import sys
from typing import List

import pytest

from skbase.testing import BaseFixtureGenerator, QuickTester
from skbase.tests.conftest import Parent

__author__: List[str] = ["yash-sangwan"]


class _NoisyTester(BaseFixtureGenerator, QuickTester):
    """Minimal test class that writes to both output streams."""

    def test_writes_to_streams(self, object_class):
        """Write a marker to stdout and to stderr."""
        sys.stdout.write("stdout-marker")
        sys.stderr.write("stderr-marker")


@pytest.mark.parametrize("bad", [42, ["a", 5], {"a": 1}])
def test_check_none_str_or_list_of_str_rejects_invalid(bad):
    """Invalid input raises; a generator passed to np.all would never raise."""
    with pytest.raises(ValueError, match="must be None, str, or list of str"):
        QuickTester._check_none_str_or_list_of_str(bad, var_name="x")


@pytest.mark.parametrize(
    "good, expected", [(None, None), ("a", ["a"]), (["a", "b"], ["a", "b"])]
)
def test_check_none_str_or_list_of_str_accepts_valid(good, expected):
    """Valid input is returned, coerced to list of str."""
    assert QuickTester._check_none_str_or_list_of_str(good, var_name="x") == expected


@pytest.mark.parametrize("verbose, muted", [(0, True), (2, False)])
def test_run_tests_mutes_stdout_and_stderr(capsys, verbose, muted):
    """Both streams are muted below verbose=2, and both are shown at verbose=2."""
    _NoisyTester().run_tests(
        Parent, tests_to_run="test_writes_to_streams", verbose=verbose
    )
    captured = capsys.readouterr()
    assert ("stdout-marker" not in captured.out) is muted
    assert ("stderr-marker" not in captured.err) is muted
