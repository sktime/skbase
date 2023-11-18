#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
""":mod:`skbase.base` contains base classes for creating parametric objects.

The included functionality makes it easy to reuse scikit-learn and
sktime design principles in your project.
"""
from typing import List

from skbase.base._base import BaseEstimator, BaseObject
from skbase.base._meta import (
    BaseMetaEstimator,
    BaseMetaEstimatorMixin,
    BaseMetaObject,
    BaseMetaObjectMixin,
)

__author__: List[str] = ["mloning", "RNKuhns", "fkiraly"]
__all__: List[str] = [
    "BaseObject",
    "BaseEstimator",
    "BaseMetaEstimator",
    "BaseMetaObject",
    "BaseMetaEstimatorMixin",
    "BaseMetaObjectMixin",
]
