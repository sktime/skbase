#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests of the functionality for working with iterables.

tests in this module incdlue:

- test_format_seq_to_str: verify that _format_seq_to_str outputs expected format.
"""

__author__ = ["RNKuhns"]
from skbase.base import BaseEstimator, BaseObject
from skbase.utils._iter import _format_seq_to_str


def test_format_seq_to_str():
    """Test _format_seq_to_str returns expected output."""
    # Test basic functionality (including ability to handle str and non-str)
    seq = [1, 2, "3", 4]
    assert _format_seq_to_str(seq) == "1, 2, 3, 4"

    # Test use of last_sep
    assert _format_seq_to_str(seq, last_sep="and") == "1, 2, 3 and 4"
    assert _format_seq_to_str(seq, last_sep="or") == "1, 2, 3 or 4"

    # Test use of different sep argument
    assert _format_seq_to_str(seq, sep=";") == "1;2;3;4"

    # Verify things work with BaseObject and BaseEstimator instances
    seq = [BaseEstimator(), BaseObject(), 1]
    assert _format_seq_to_str(seq) == "BaseEstimator(), BaseObject(), 1"

    # Test use of last_sep
    assert (
        _format_seq_to_str(seq, last_sep="and") == "BaseEstimator(), BaseObject() and 1"
    )
    assert (
        _format_seq_to_str(seq, last_sep="or") == "BaseEstimator(), BaseObject() or 1"
    )

    # Test use of different sep argument
    assert _format_seq_to_str(seq, sep=";") == "BaseEstimator();BaseObject();1"
