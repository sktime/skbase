#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tools for validating types."""
import inspect
from collections.abc import Iterable, Sequence
from typing import Any, List, Optional, Tuple, Union

from skbase.utils._iter import _format_seq_to_str

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = ["check_sequence", "check_type"]


def check_type(
    input_: Any,
    expected_type: type,
    allow_none: bool = False,
    input_name: Optional[str] = None,
    use_subclass: bool = False,
) -> Any:
    """Check the input is the expected type.

    Parameters
    ----------
    input_ : Any
        The input to be type checked.
    expected_type : type
        The type that `input_` is expected to be.
    allow_none : bool, default=False
        Whether `input_` can be None in addition to being instance of `expected_type`.
    input_name : str, default=None
        The name to use when referring to `input_` in any raised error messages.
        If None, then "input_" is used as `input_name`.
    use_subclass : bool, default=False
        Whether to check the type using issubclass instead of isinstance.

        - If True, then check uses issubclass.
        - If False (default), then check uses isinstance.

    Returns
    -------
    input_ : Any
        The input object.
    """
    # process expected_type parameter
    if not isinstance(expected_type, (type, tuple)):
        msg = " ".join(
            [
                "`expected_type` should be type or tuple[type, ...],"
                f"but found {type(expected_type)}."
            ]
        )
        raise ValueError(msg)

    # process input_name parameter
    if input_name is None:
        input_name = "input_"
    else:
        if not isinstance(input_name, str):
            raise ValueError(
                f"`input_name` should be str, but found {type(input_name)}."
            )
    # Check the type of input_
    type_check = issubclass if use_subclass else isinstance
    if (not allow_none and input_ is None) or not type_check(input_, expected_type):
        chk_msg = "subclass type" if use_subclass else "be type"
        type_msg = f"{expected_type} or None" if allow_none else f"{expected_type}"
        raise ValueError(
            f"`{input_name}` should {chk_msg} {type_msg}, but found {type(input_name)}."
        )
    return input_


def check_sequence(
    input_seq: Any,
    sequence_type: Union[type, Tuple[type]] = Sequence,
    element_type: Optional[Union[type, Tuple[type, ...]]] = None,
    coerce_to_type: type = None,
    sequence_name: str = None,
) -> Sequence[Any]:
    """Check whether an object is a sequence of expected type.

    If `element_type` is supplied all elements are also checked against provided types.

    Parameters
    ----------
    input_seq : Any
        The input sequence to be validated.
    sequence_type : type or tuple[type], default=Sequence
        The allowed sequence type that `seq` can be an instance of.
    element_type : type or tuple[type], default=None
        The allowed type(s) for elements of `seq`.
    coerce_to_type : sequence type
        The sequence type that the output sequence should be coerced to. If None,
        then the output sequence is the same as input sequence (including type).
    sequence_name : str, default=None
        Name of `input_seq` to use if error messages are raised.

    Returns
    -------
    input_seq : Sequence
        The input sequence.

    Raises
    ------
    ValueError :
        If `seq` is not instance of `sequence_type` or ``element_type is not None`` and
        all elements are not instances of `element_type`.
    """
    if sequence_name is None:
        sequence_name = "input_seq"
    else:
        check_type(sequence_name, str, input_name="sequence_name")

    if isinstance(element_type, type):
        element_allow_none = False
    elif isinstance(element_type, tuple) and all(
        isinstance(e, type) for e in element_type
    ):
        element_allow_none = None in element_type
        if element_allow_none:
            element_type = tuple(e for e in element_type if e is not None)
    else:
        raise ValueError(
            " ".join(
                [
                    "`element_type` should be type, tuple of types or None,"
                    f"but found type {type(element_type)}."
                ]
            )
        )
    # Raise error if input is not correct sequence type
    if not isinstance(input_seq, sequence_type):
        invalid_seq_type_msg = " ".join(
            [
                f"`{sequence_name}` is not a valid. Expected sequence of type"
                f"{sequence_type}, but found {type(input_seq)}.",
            ]
        )
        raise ValueError(invalid_seq_type_msg)

    # Given correct sequence type, optionall check element types
    if element_type is None:
        return input_seq
    else:
        if element_allow_none:
            invalid_elements = [
                e for e in input_seq if not (e is None or isinstance(e, element_type))
            ]
        else:
            invalid_elements = [e for e in input_seq if not isinstance(e, element_type)]
        if len(invalid_elements) > 0:
            invalid_elements_str = _format_seq_to_str(invalid_elements, last_sep="and")
            invalid_elements_msg = " ".join(
                [
                    f"`{sequence_name}` is not a valid. Expected all elements to be"
                    f"type {element_type}, but found elements {invalid_elements_str}."
                ]
            )
            raise ValueError(invalid_elements_msg)

    if coerce_to_type is not None:
        if coerce_to_type not in (list, tuple):
            raise ValueError("`coerce_to_type` should be")
        return coerce_to_type(input_seq)
    return input_seq


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
