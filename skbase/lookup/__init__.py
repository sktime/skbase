#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tools to lookup information on code artifacts in a Python package or module.

This module exports the following functions:

package_metadata()
    Walk package and return metadata on included classes and functions by module.
    Users can optionally filter the information to return.
all_objects()
    Lookup BaseObject descendants in a package or module. Users can optionally filter
    the information to return.
"""
# all_objects is based on the sktime all_estimator retrieval utility, which
# is based on the sklearn estimator retrieval utility of the same name
# See https://github.com/scikit-learn/scikit-learn/blob/main/COPYING and
# https://github.com/sktime/sktime/blob/main/LICENSE
from typing import List

from skbase.lookup._lookup import all_objects, get_package_metadata

__all__: List[str] = ["all_objects", "get_package_metadata"]
__author__: List[str] = [
    "fkiraly",
    "mloning",
    "katiebuc",
    "miraep8",
    "xloem",
    "rnkuhns",
]
