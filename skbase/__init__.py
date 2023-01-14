#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
""":mod:`skbase` contains tools for creating and working with parametric objects.

The included functionality makes it easy to re-use scikit-learn and
sktime design principles in your project.
"""
from typing import List

from skbase.base import BaseEstimator, BaseMetaEstimator, BaseObject
from skbase.lookup import all_objects

__version__: str = "0.3.0"

__author__: List[str] = ["mloning", "RNKuhns", "fkiraly"]
__all__: List[str] = ["BaseEstimator", "BaseMetaEstimator", "BaseObject", "all_objects"]
