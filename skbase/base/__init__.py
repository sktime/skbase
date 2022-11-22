#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
""":mod:`skbase.base` contains base classes for creating parametric objects.

The included functionality makes it easy to re-use scikit-learn and
sktime design principles in your project.
"""

__author__ = ["mloning", "RNKuhns", "fkiraly"]
__all__ = [
    "BaseObject",
    "BaseEstimator",
    "_HeterogenousMetaEstimator",
]

from skbase.base._base import BaseEstimator, BaseObject
from skbase.base._meta import _HeterogenousMetaEstimator
