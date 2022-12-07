#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Functionality used through `skbase`."""
from typing import List

from skbase.utils._nested_iter import flatten, is_flat, unflat_len, unflatten

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = ["flatten", "is_flat", "unflat_len", "unflatten"]
