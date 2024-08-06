# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests of stdout_mute and stderr_mute."""
import io
import sys
from contextlib import redirect_stderr, redirect_stdout

import pytest

from skbase.utils.stderr_mute import StderrMute
from skbase.utils.stdout_mute import StdoutMute

__author__ = ["XinyuWu"]


@pytest.mark.parametrize(
    "mute, expected", [(True, ["", ""]), (False, ["test stdout", "test sterr"])]
)
def test_std_mute(mute, expected):
    """Test StderrMute."""
    stderr_io = io.StringIO()
    stdout_io = io.StringIO()

    try:
        with redirect_stderr(stderr_io), redirect_stdout(stdout_io):
            with StderrMute(mute), StdoutMute(mute):
                sys.stdout.write("test stdout")
                sys.stderr.write("test sterr")
                1 / 0
    except ZeroDivisionError:
        assert expected == [stdout_io.getvalue(), stderr_io.getvalue()]
