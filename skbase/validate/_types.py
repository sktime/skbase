#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tools for validating types."""
import inspect
from collections.abc import Iterable
from typing import List

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = []


def _check_list_of_str(obj, name="obj"):
    """Check whether obj is a list of str.

    Parameters
    ----------
    obj : any object, check whether is list of str
    name : str, default="obj", name of obj to display in error message

    Returns
    -------
    obj, unaltered

    Raises
    ------
    TypeError if obj is not list of str
    """
    if not isinstance(obj, list) or not all(isinstance(x, str) for x in obj):
        raise TypeError(f"{name} must be a list of str")
    return obj


def _check_list_of_str_or_error(arg_to_check, arg_name):
    """Check that certain arguments are str or list of str.

    Parameters
    ----------
    arg_to_check: any
        Argument we are testing the type of.
    arg_name: str,
        name of the argument we are testing, will be added to the error if
        ``arg_to_check`` is not a str or a list of str.

    Returns
    -------
    arg_to_check: list of str,
        if arg_to_check was originally a str it converts it into a list of str
        so that it can be iterated over.

    Raises
    ------
    TypeError if arg_to_check is not a str or list of str.
    """
    # check that return_tags has the right type:
    if isinstance(arg_to_check, str):
        arg_to_check = [arg_to_check]
    elif not isinstance(arg_to_check, list) or not all(
        isinstance(value, str) for value in arg_to_check
    ):
        raise TypeError(
            f"Input error. Argument {arg_name} must be either\
             a str or list of str"
        )
    return arg_to_check


def _check_iterable_of_class_or_error(arg_to_check, arg_name, coerce_to_list=False):
    """Check that certain arguments are class or list of class.

    Parameters
    ----------
    arg_to_check: any
        Argument we are testing the type of.
    arg_name: str
        name of the argument we are testing, will be added to the error if
        ``arg_to_check`` is not a str or a list of str.
    coerce_to_list : bool, default=False
        Whether `arg_to_check` should be coerced to a list prior to return.

    Returns
    -------
    arg_to_check: list of class,
        If `arg_to_check` was originally a class it converts it into a list
        containing the class so it can be iterated over. Otherwise,
        `arg_to_check` is returned.

    Raises
    ------
    TypeError:
        If `arg_to_check` is not a class or iterable of class.
    """
    # check that return_tags has the right type:
    if inspect.isclass(arg_to_check):
        arg_to_check = [arg_to_check]
    elif not (
        isinstance(arg_to_check, Iterable)
        and all(inspect.isclass(value) for value in arg_to_check)
    ):
        raise TypeError(
            f"Input error. Argument {arg_name} must be either\
             a class or an iterable of classes"
        )
    elif coerce_to_list:
        arg_to_check = list(arg_to_check)
    return arg_to_check
