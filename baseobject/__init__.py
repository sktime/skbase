#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: BaseObject developers, BSD-3-Clause License (see LICENSE file)
""":mod:`baseobject` contains classes with scikit-learn and sktime design principles."""

__version__ = "0.1.0"

__author__ = ["mloning", "RNKuhns", "fkiraly"]
__all__ = [
    "BaseObject",
    "BaseEstimator",
    "_HeterogenousMetaEstimator",
    "all_objects",
    "get_package_metadata",
]

from baseobject._base import BaseEstimator, BaseObject
from baseobject._lookup import all_objects, get_package_metadata
from baseobject._meta import _HeterogenousMetaEstimator
