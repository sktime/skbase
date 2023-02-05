#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Functionality for working with sequences."""
import re
from collections.abc import Sequence
from typing import Any, List, Optional, Union

from skbase.utils._nested_iter import _remove_single

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = ["_scalar_to_seq", "_format_seq_to_str"]


def _scalar_to_seq(scalar: Any, sequence_type: type = None) -> Sequence:
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


def _format_seq_to_str(
    seq: Union[str, Sequence],
    sep: str = ", ",
    last_sep: Optional[str] = None,
    remove_type_text: bool = False,
) -> str:
    """Format a sequence to a string of delimitted elements.

    This is useful to format sequences into a pretty printing format for
    creating error messages or warnings.

    Parameters
    ----------
    seq : Sequence
        The input sequence to convert to a str of the elements separated by `sep`.
    sep : str
        The separator to use when creating the str output.
    last_sep : str, default=None
        The separator to use prior to last element.

        - If None, then `sep` is used. So (7, 9, 11) return "7", "9", "11" for
          ``sep=", "``.
        - If last_sep is a str, then it is used prior to last element. So
          (7, 9, 11) would be "7", "9" and "11" if ``last_sep="and"``.

    remove_type_text : bool, default=False
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
    >>> from skbase.utils._iter import _format_seq_to_str
    >>> seq = [1, 2, 3, 4]
    >>> _format_seq_to_str(seq)
    '1, 2, 3, 4'
    >>> _format_seq_to_str(seq, last_sep="and")
    '1, 2, 3 and 4'
    """
    if isinstance(seq, str):
        return seq
    # Allow casting of scalars to strings
    elif isinstance(seq, (int, float, bool)):
        return str(seq)
    elif not isinstance(seq, Sequence):
        raise ValueError("`seq` must be a sequence or scalar str, int, float or bool.")

    seq_str = [str(e) for e in seq]
    if remove_type_text:
        for idx, s in enumerate(seq_str):
            m = re.match("^<class '(.*)'>$", s)
            if m:
                seq_str[idx] = m[1]

    if last_sep is None:
        output_str = sep.join(seq_str)
    else:
        if len(seq_str) == 1:
            output_str = _remove_single(seq_str)
        else:
            output_str = sep.join(e for e in seq_str[:-1])
            output_str = output_str + f" {last_sep} " + seq_str[-1]

    return output_str
