#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Miscellaneous functionality used through `skbase`."""
from typing import List

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = []


def _remove_single(x):
    """Remove tuple wrapping from singleton.

    Parameters
    ----------
    x : tuple

    Returns
    -------
    x[0] if x is a singleton, otherwise x
    """
    if len(x) == 1:
        return x[0]
    else:
        return x
