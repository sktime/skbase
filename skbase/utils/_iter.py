#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Functionality for working with sequences."""
from typing import List, Optional, Sequence

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = []


def _format_seq_to_str(
    seq: Sequence, sep: str = ", ", last_sep: Optional[str] = None
) -> str:
    """Format a sequence to a string of comma separated elements.

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

    Returns
    -------
    seq_str : str
        The sequence of inputs converted to a string. For example, if `seq`
        is (7, 9, "cart") and ``last_sep is None`` then the output is
        "7", "9", "cart".

    Examples
    --------
    >>> seq = [1, 2, 3, 4]
    >>> _format_seq_to_str(seq)
    '1, 2, 3, 4'
    >>> _format_seq_to_str(seq, last_sep="and")
    '1, 2, 3 and 4'
    """
    if last_sep is None:
        seq_str = sep.join(str(e) for e in seq)
    else:
        seq_str = sep.join(str(e) for e in seq[:-1])
        seq_str = seq_str + f" {last_sep} " + str(seq[-1])
    return seq_str
