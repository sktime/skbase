#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tools for validating types."""
import collections
import inspect
from typing import Any, List, Optional, Sequence, Tuple, Union

from skbase.utils._iter import _format_seq_to_str, _remove_type_text, _scalar_to_seq

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = ["check_sequence", "check_type", "is_sequence"]


def check_type(
    input_: Any,
    expected_type: type,
    allow_none: bool = False,
    input_name: Optional[str] = None,
    use_subclass: bool = False,
) -> Any:
    """Check the input is the expected type.

    Validates that the input is the type specified in `expected_type`, while optionally
    allowing None values as well (if ``allow_none=True``). For flexibility,
    the check can use ``issubclass`` instead of ``isinstance`` if ``use_subclass=True``.

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
        If None, then "input" is used as `input_name`.
    use_subclass : bool, default=False
        Whether to check the type using issubclass instead of isinstance.

        - If True, then check uses issubclass.
        - If False (default), then check uses isinstance.

    Returns
    -------
    Any
        The input object.

    Raises
    ------
    TypeError
        If input does match expected type using isinstance by default
        or using issubclass in check if ``use_subclass=True``.

    Examples
    --------
    >>> from skbase.base import BaseEstimator, BaseObject
    >>> from skbase.validate import check_type
    >>> check_type(7, expected_type=int)
    7
    >>> check_type(7.2, expected_type=(int, float))
    7.2
    >>> check_type(BaseEstimator(), BaseObject)
    BaseEstimator()
    >>> check_type(BaseEstimator, expected_type=BaseObject, use_subclass=True)
    <class 'skbase.base._base.BaseEstimator'>

    An error is raised if the input is not the expected type

    >>> check_type(7, expected_type=str) # doctest: +SKIP
    TypeError: `input` should be type <class 'str'>, but found <class 'str'>.
    """
    # process expected_type parameter
    if not isinstance(expected_type, (type, tuple)):
        msg = " ".join(
            [
                "`expected_type` should be type or tuple[type, ...],"
                f"but found {_remove_type_text(expected_type)}."
            ]
        )
        raise TypeError(msg)

    # Assign default name to input_name parameter in case it is None
    if input_name is None:
        input_name = "input"

    # Check the type of input_
    type_check = issubclass if use_subclass else isinstance
    if (allow_none and input_ is None) or type_check(input_, expected_type):
        return input_
    else:
        chk_msg = "subclass type" if use_subclass else "be type"
        expected_type_str = _remove_type_text(expected_type)
        input_type_str = _remove_type_text(type(input_))
        if allow_none:
            type_msg = f"{expected_type_str} or None"
        else:
            type_msg = f"{expected_type_str}"
        raise TypeError(
            f"`{input_name}` should {chk_msg} {type_msg}, but found {input_type_str}."
        )


def _convert_scalar_seq_type_input_to_tuple(
    type_input: Optional[Union[type, Tuple[type, ...]]],
    none_default: Optional[type] = None,
    type_input_subclass: Optional[type] = None,
    input_name: str = None,
) -> Tuple[type, ...]:
    """Convert input that is scalar or sequence of types to always be a tuple."""
    if none_default is None:
        none_default = collections.abc.Sequence

    seq_output: Tuple[type, ...]
    if type_input is None:
        seq_output = (none_default,)
    # if a sequence of types received as sequence_type, convert to tuple of types
    elif isinstance(type_input, collections.abc.Sequence) and all(
        isinstance(e, type) for e in type_input
    ):
        seq_output = tuple(type_input)
    elif (isinstance(type_input, type) or inspect.isclass(type_input)) and (
        type_input_subclass is None or issubclass(type_input, type_input_subclass)
    ):
        seq_output = (type_input,)
    else:
        name_str = "type_input" if input_name is None else input_name
        raise TypeError(f"`{name_str}` should be a type or tuple of types.")

    return seq_output


def is_sequence(
    input_seq: Any,
    sequence_type: Optional[Union[type, Tuple[type, ...]]] = None,
    element_type: Optional[Union[type, Tuple[type, ...]]] = None,
) -> bool:
    """Indicate if an object is a sequence with optional check of element types.

    If `element_type` is supplied all elements are also checked against provided types.

    Parameters
    ----------
    input_seq : Any
        The input sequence to be validated.
    sequence_type : type or tuple[type, ...], default=None
        The allowed sequence type(s) that `input_seq` can be an instance of.

        - If None, then collections.abc.Sequence is used (all sequence types are valid)
        - If `sequence_type` is a type or tuple of types, then only the specified
          types are considered valid.

    element_type : type or tuple[type], default=None
        The allowed type(s) for elements of `input_seq`.

        - If None, then the elements of `input_seq` are not checked when determining
          if `input_seq` is a valid sequence.
        - If `element_type` is a type or tuple of types, then the elements of
          `input_seq` are checked to make sure they are all instances of
          the supplied `element_type`.

    Returns
    -------
    bool
        Whether the input is a valid sequence based on the supplied `sequence_type`
        and `element_type`.

    Examples
    --------
    >>> from skbase.base import BaseEstimator, BaseObject
    >>> from skbase.validate import is_sequence
    >>> is_sequence([1, 2, 3])
    True
    >>> is_sequence(7)
    False

    Generators are not sequences

    >>> is_sequence((c for c in [1, 2, 3]))
    False

    The expected sequence type can be included in the check

    >>> is_sequence([1, 2, 3, 4], sequence_type=list)
    True
    >>> is_sequence([1, 2, 3, 4], sequence_type=tuple)
    False

    The type of the elements can also be checked

    >>> is_sequence([1, 2, 3], element_type=int)
    True
    >>> is_sequence([1, 2, 3, 4], sequence_type=list, element_type=int)
    True
    >>> is_sequence([1, 2, 3, 4], sequence_type=list, element_type=float)
    False
    >>> is_sequence([1, 2, 3, 4], sequence_type=list, element_type=(int, float))
    True
    >>> is_sequence((BaseObject(), BaseEstimator()), element_type=BaseObject)
    True
    """
    sequence_type_ = _convert_scalar_seq_type_input_to_tuple(
        sequence_type,
        input_name="sequence_type",
        type_input_subclass=collections.abc.Sequence,
    )

    is_valid_sequence = isinstance(input_seq, sequence_type_)

    # Optionally verify elements have correct types
    if element_type is not None:
        element_type_ = _convert_scalar_seq_type_input_to_tuple(
            element_type, input_name="element_type"
        )
        element_types_okay = all(isinstance(e, element_type_) for e in input_seq)
        if not element_types_okay:
            is_valid_sequence = False

    return is_valid_sequence


def check_sequence(
    input_seq: Sequence[Any],
    sequence_type: Optional[Union[type, Tuple[type, ...]]] = None,
    element_type: Optional[Union[type, Tuple[type, ...]]] = None,
    coerce_output_type_to: type = None,
    coerce_scalar_input: bool = False,
    sequence_name: str = None,
) -> Sequence[Any]:
    """Check whether an object is a sequence with optional check of element types.

    If `element_type` is supplied all elements are also checked against provided types.

    Parameters
    ----------
    input_seq : Any
        The input sequence to be validated.
    sequence_type : type or tuple[type], default=None
        The allowed sequence type that `seq` can be an instance of.
    element_type : type or tuple[type], default=None
        The allowed type(s) for elements of `seq`.
    coerce_output_type_to : sequence type
        The sequence type that the output sequence should be coerced to.

        - If None, then the output sequence is the same as input sequence.
        - If a sequence type (e.g., list, tuple) is provided then the output sequence
          is coerced to that type.

    coerce_scalar_input : bool, default=False
        Whether scalar input should be coerced to a sequence type prior to running
        the check. If True, a scalar input like will be coerced to a tuple containing
        a single scalar. To output a sequence type other than a tuple, set the
        `coerce_output_type_to` keyword to the desired sequence type (e.g., list).
    sequence_name : str, default=None
        Name of `input_seq` to use if error messages are raised.

    Returns
    -------
    Sequence
        The input sequence if has expected type.

    Raises
    ------
    TypeError :
        If `seq` is not instance of `sequence_type` or ``element_type is not None`` and
        all elements are not instances of `element_type`.

    Examples
    --------
    >>> from skbase.base import BaseEstimator, BaseObject
    >>> from skbase.validate import is_sequence

    >>> check_sequence([1, 2, 3])
    [1, 2, 3]

    Generators are not sequences so an error is raised

    >>> check_sequence((c for c in [1, 2, 3])) # doctest: +SKIP

    The check can require a certain type of sequence

    >>> check_sequence([1, 2, 3, 4], sequence_type=list)
    [1, 2, 3, 4]

    Expected to raise and error because the input is not a tuple

    >>> check_sequence([1, 2, 3, 4], sequence_type=tuple) # doctest: +SKIP

    It is also possible to check the type of sequence elements

    >>> check_sequence([1, 2, 3], element_type=int)
    [1, 2, 3]
    >>> check_sequence([1, 2, 3, 4], sequence_type=list, element_type=(int, float))
    [1, 2, 3, 4]

    The check also works with BaseObjects

    >>> check_sequence((BaseObject(), BaseEstimator()), element_type=BaseObject)
    (BaseObject(), BaseEstimator())
    """
    if coerce_scalar_input:
        if isinstance(sequence_type, tuple):
            # If multiple sequence types allowed then use first one
            input_seq = _scalar_to_seq(input_seq, sequence_type=sequence_type[0])
        else:
            input_seq = _scalar_to_seq(input_seq, sequence_type=sequence_type)

    is_valid_sequence = is_sequence(
        input_seq,
        sequence_type=sequence_type,
        element_type=element_type,
    )
    # Raise error is format is not expected.
    if not is_valid_sequence:
        name_str = "Input sequence" if sequence_name is None else f"`{sequence_name}`"
        if sequence_type is None:
            seq_str = "a sequence"
        else:
            sequence_type_ = _convert_scalar_seq_type_input_to_tuple(
                sequence_type,
                input_name="sequence_type",
                type_input_subclass=collections.abc.Sequence,
            )
            seq_str = _format_seq_to_str(
                sequence_type_, last_sep="or", remove_type_text=True
            )

        msg = f"Invalid sequence: {name_str} expected to be a {seq_str}."

        if element_type is not None:
            element_type_ = _convert_scalar_seq_type_input_to_tuple(
                element_type, input_name="element_type"
            )
            element_str = _format_seq_to_str(
                element_type_, last_sep="or", remove_type_text=True
            )
            msg = msg[:-1] + f" with elements of type {element_str}."

        raise TypeError(msg)

    if coerce_output_type_to is not None:
        return coerce_output_type_to(input_seq)

    return input_seq
