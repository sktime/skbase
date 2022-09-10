#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
""":mod:`skbase` contains tools for creating and working with parametric objects.

The included functionality makes it easy to re-use scikit-learn and
sktime design principles in your project.
"""

__version__ = "0.2.0"

__author__ = ["mloning", "RNKuhns", "fkiraly"]
__all__ = [
    "BaseObject",
    "BaseEstimator",
    "_HeterogenousMetaEstimator",
    "all_objects",
    "get_package_metadata",
]

from skbase._base import BaseEstimator, BaseObject
from skbase._lookup import all_objects, get_package_metadata
from skbase._meta import _HeterogenousMetaEstimator
