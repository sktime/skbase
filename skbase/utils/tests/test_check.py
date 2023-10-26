#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests of the utility functionality for performing various checks.

tests in this module include:

- test_is_scalar_nan_output to verify _is_scalar_nan outputs expected value for
  different inputs.
"""
from skbase.utils._check import _is_scalar_nan

__author__ = ["RNKuhns"]


def test_is_scalar_nan_output():
    """Test that _is_scalar_nan outputs expected value for different inputs."""
    import numpy as np

    assert _is_scalar_nan(np.nan) is True
    assert _is_scalar_nan(float("nan")) is True
    assert _is_scalar_nan(None) is False
    assert _is_scalar_nan("") is False
    assert _is_scalar_nan([np.nan]) is False
