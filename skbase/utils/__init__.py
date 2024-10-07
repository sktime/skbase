#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Utility functionality used through `skbase`."""
from typing import List

from skbase.utils._iter import make_strings_unique
from skbase.utils._nested_iter import flatten, is_flat, unflat_len, unflatten
from skbase.utils._utils import subset_dict_keys
from skbase.utils.deep_equals import deep_equals
from skbase.utils.random_state import (
    check_random_state,
    sample_dependent_seed,
    set_random_state,
)

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = [
    "check_random_state",
    "deep_equals",
    "flatten",
    "is_flat",
    "make_strings_unique",
    "sample_dependent_seed",
    "set_random_state",
    "subset_dict_keys",
    "unflat_len",
    "unflatten",
]
