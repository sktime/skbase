#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
""":mod:`skbase` contains tools for creating and working with parametric objects.

The included functionality makes it easy to re-use scikit-learn and
sktime design principles in your project.
"""
import warnings

from skbase.base import BaseEstimator, BaseObject, _HeterogenousMetaEstimator
from skbase.lookup import all_objects, get_package_metadata

__version__ = "0.2.0"

__author__ = ["mloning", "RNKuhns", "fkiraly"]
__all__ = [
    "BaseObject",
    "BaseEstimator",
    "_HeterogenousMetaEstimator",
    "all_objects",
    "get_package_metadata",
]

warnings.warn(
    " ".join(
        [
            "Importing from the `skbase` module is deprecated as of version 0.3.0.",
            "Ability to import from `skbase` will be removed in version 0.5.0."
            "Import BaseObject, BaseEstimator, and _HeterogenousMetaEstimator"
            "from skbase.base. Import lookup functionality "
            "(all_objects, get_package_metadata) from skbase.lookup.",
        ]
    ),
    DeprecationWarning,
)
