#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Utility functionality used through `skbase`."""
from typing import List

from skbase.utils._iter import make_strings_unique
from skbase.utils._nested_iter import flatten, is_flat, unflat_len, unflatten
from skbase.utils._utils import subset_dict_keys

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = [
    "flatten",
    "is_flat",
    "make_strings_unique",
    "subset_dict_keys",
    "unflat_len",
    "unflatten",
]
