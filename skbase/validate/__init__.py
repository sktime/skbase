#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tools for validating and comparing BaseObjects and collections of BaseObjects."""
from typing import List

from skbase.validate._named_objects import (
    check_iterable_named_objects,
    is_iterable_named_objects,
)

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = ["check_iterable_named_objects", "is_iterable_named_objects"]
