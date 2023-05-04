# -*- coding: utf-8 -*-
"""Tests to run without pytest, to check pytest isolation."""
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)

from skbase.base import BaseObject
from skbase.lookup import all_objects

MODULES_TO_IGNORE = ("tests", "dependencies", "all")

# all_objectscrawls all modules excepting pytest test files
# if it encounters an unisolated import, it will throw an exception
results = all_objects()

# try to run all methods of BaseObject without arguments
# very basic test, but needs to run without pytest
METHODS = [
    "clone",
    "get_params",
    "reset",
    "get_param_names",
    "get_param_defaults",
    "get_params",
    "get_class_tags",
    "get_tags",
    "get_config",
    "get_test_params",
    "create_test_instance",
    "create_test_instances_and_names",
    "is_composite",
]

mybo = BaseObject()
for method in METHODS:
    getattr(mybo, method)
