#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Functionality for working with sequences."""
import collections
import re
from collections.abc import Sequence

from skbase.utils._nested_iter import _remove_single, flatten, is_flat, unflatten

__author__ = ["fkiraly", "RNKuhns"]
__all__ = [
    "_scalar_to_seq",
    "_remove_type_text",
    "_format_seq_to_str",
    "make_strings_unique",
]


def _scalar_to_seq(scalar, sequence_type=None):
    """Convert a scalar input to a sequence.

    If the input is already a sequence it is returned unchanged. Unlike standard
    Python, a string is treated as a scalar instead of a sequence.

    Parameters
    ----------
    scalar : Any
        A scalar input to be converted to a sequence.
    sequence_type : type, default=None
        A sequence type (e.g., list, tuple) that is used to set the return type. This
        is ignored if `scalar` is already a sequence other than a str (which is
        treated like a scalar type for this function instead of sequence of
        characters).

        - If None, then the returned sequence will be a tuple containing a single
          scalar element.
        - If `sequence_type` is a valid sequence type then the returned
          sequence will be a sequence of that type containing the single scalar
          value.

    Returns
    -------
    Sequence
        A sequence of the specified `sequence_type` that contains just the single
        scalar value.

    Examples
    --------
    >>> from skbase.utils._iter import _scalar_to_seq
    >>> _scalar_to_seq(7)
    (7,)
    >>> _scalar_to_seq("some_str")
    ('some_str',)
    >>> _scalar_to_seq("some_str", sequence_type=list)
    ['some_str']
    >>> _scalar_to_seq((1, 2))
    (1, 2)
    """
    # We'll treat str like regular scalar and not a sequence
    if isinstance(scalar, Sequence) and not isinstance(scalar, str):
        return scalar
    elif sequence_type is None:
        return (scalar,)
    elif issubclass(sequence_type, Sequence) and sequence_type != Sequence:
        # Note calling (scalar,) is done to avoid str unpacking
        return sequence_type((scalar,))  # type: ignore
    else:
        raise ValueError(
            "`sequence_type` must be a subclass of collections.abc.Sequence."
        )


def _remove_type_text(input_):
    """Remove <class > wrapper from printed type str."""
    if not isinstance(input_, str):
        input_ = str(input_)

    m = re.match("^<class '(.*)'>$", input_)
    if m:
        return m[1]
    else:
        return input_


def _format_seq_to_str(seq, sep=", ", last_sep=None, remove_type_text=True):
    """Format a sequence to a string of delimitted elements.

    This is useful to format sequences into a pretty printing format for
    creating error messages or warnings.

    Parameters
    ----------
    seq : Sequence
        The input sequence to convert to a str of the elements separated by `sep`.
    sep : str, default=", "
        The separator to use when creating the str output.
    last_sep : str, default=None
        The separator to use prior to last element.

        - If None, then `sep` is used. So (7, 9, 11) return "7", "9", "11" for
          ``sep=", "``.
        - If last_sep is a str, then it is used prior to last element. So
          (7, 9, 11) would be "7", "9" and "11" if ``last_sep="and"``.

    remove_type_text : bool, default=True
        Whether to remove the <class > text wrapping the class type name, when
        formatting types.

        - If True, then input sequence [list, tuple] returns "list, tuple"
        - If False, then input sequence [list, tuple] returns
          "<class 'list'>, <class 'tuple'>".

    Returns
    -------
    str
        The sequence of inputs converted to a string. For example, if `seq`
        is (7, 9, "cart") and ``last_sep is None`` then the output is
        "7", "9", "cart".

    Examples
    --------
    >>> from skbase.base import BaseEstimator, BaseObject
    >>> from skbase.utils._iter import _format_seq_to_str
    >>> seq = [1, 2, 3, 4]
    >>> _format_seq_to_str(seq)
    '1, 2, 3, 4'
    >>> _format_seq_to_str(seq, last_sep="and")
    '1, 2, 3 and 4'
    >>> _format_seq_to_str((BaseObject, BaseEstimator))
    'skbase.base._base.BaseObject, skbase.base._base.BaseEstimator'
    """
    if isinstance(seq, str):
        return seq
    # Allow casting of scalars to strings
    elif isinstance(seq, (int, float, bool, type)):
        return _remove_type_text(seq)
    elif not isinstance(seq, Sequence):
        raise TypeError(
            "`seq` must be a sequence or scalar str, int, float, bool or class."
        )

    seq_str = [str(e) for e in seq]
    if remove_type_text:
        seq_str = [_remove_type_text(s) for s in seq_str]

    if last_sep is None:
        output_str = sep.join(seq_str)
    else:
        if len(seq_str) == 1:
            output_str = _remove_single(seq_str)
        else:
            output_str = sep.join(e for e in seq_str[:-1])
            output_str = output_str + f" {last_sep} " + seq_str[-1]

    return output_str


# copied from sktime _HeterogenousMetaEstimator._make_strings_unique
def make_strings_unique(str_list):
    """Make a list or tuple of strings unique by appending number of occurrence.

    Supports making string elements unique for nested list/tuple input.

    Parameters
    ----------
    str_list : nested list/tuple structure with string elements
        The list or tuple with string elements that should be made unique.

    Returns
    -------
    list[str] | tuple[str]
        The input strings coerced to have unique names.

        - If no duplicates then the output list/tuple is same as input.
        - Otherwise, the integer number of occurrence is appended onto duplicate
          strings. If this results in duplicates (b/c another string in input had
          the name of a string and integer of occurrence) this is repeated until
          no duplicates exist.

    Examples
    --------
    >>> from skbase.utils import make_strings_unique
    >>> some_strs = ["abc", "abc", "bcd"]
    >>> make_strings_unique(some_strs)
    ['abc_1', 'abc_2', 'bcd']
    >>> some_strs = ["abc", "abc", "bcd", "abc_1"]
    >>> make_strings_unique(some_strs)
    ['abc_1_1', 'abc_2', 'bcd', 'abc_1_2']
    """
    # if strlist is not flat, flatten and apply method, then unflatten
    if not is_flat(str_list):
        flat_str_list = flatten(str_list)
        unique_flat_str_list = make_strings_unique(flat_str_list)
        unique_strs = unflatten(unique_flat_str_list, str_list)
        return unique_strs

    # if strlist is a tuple, convert to list, apply this function, then convert back
    if isinstance(str_list, tuple):
        unique_strs = make_strings_unique(list(str_list))
        unique_strs = tuple(unique_strs)
        return unique_strs

    # now we can assume that strlist is a flat list
    # if already unique, just return
    if len(set(str_list)) == len(str_list):
        return str_list

    str_count = collections.Counter(str_list)
    # if any duplicates, we append _integer of occurrence to non-uniques
    now_count: collections.Counter = collections.Counter()
    unique_strs = str_list
    for i, x in enumerate(unique_strs):
        if str_count[x] > 1:
            now_count.update([x])
            unique_strs[i] = x + "_" + str(now_count[x])

    # repeat until all are unique
    #   the algorithm recurses, but will always terminate
    #   because potential clashes are lexicographically increasing
    return make_strings_unique(unique_strs)
