#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Functionality for working with nested sequences."""
from typing import List

__author__: List[str] = ["RNKuhns", "fkiraly"]
__all__: List[str] = ["flatten", "is_flat", "unflat_len", "unflatten"]


def _remove_single(x):
    """Remove tuple wrapping from singleton.

    Parameters
    ----------
    x : tuple

    Returns
    -------
    x[0] if x is a singleton, otherwise x
    """
    if len(x) == 1:
        return x[0]
    else:
        return x


def flatten(obj):
    """Flatten nested list/tuple structure.

    Parameters
    ----------
    obj: nested list/tuple structure

    Returns
    -------
    list or tuple, tuple if obj was tuple, list otherwise
        flat iterable, containing non-list/tuple elements in obj in same order as in obj

    Example
    -------
    >>> flatten([1, 2, [3, (4, 5)], 6])
    [1, 2, 3, 4, 5, 6]
    """
    if not isinstance(obj, (list, tuple)):
        return [obj]
    else:
        return type(obj)([y for x in obj for y in flatten(x)])


def unflatten(obj, template):
    """Invert flattening, given template for nested list/tuple structure.

    Parameters
    ----------
    obj : list or tuple of elements
    template : nested list/tuple structure
        number of non-list/tuple elements of obj and template must be equal

    Returns
    -------
    rest : list or tuple of elements
        has element bracketing exactly as `template`
            and elements in sequence exactly as `obj`

    Example
    -------
    >>> unflatten([1, 2, 3, 4, 5, 6], [6, 3, [5, (2, 4)], 1])
    [1, 2, [3, (4, 5)], 6]
    """
    if not isinstance(template, (list, tuple)):
        return obj[0]

    list_or_tuple = type(template)
    ls = [unflat_len(x) for x in template]
    for i in range(1, len(ls)):
        ls[i] += ls[i - 1]
    ls = [0] + ls

    res = [unflatten(obj[ls[i] : ls[i + 1]], template[i]) for i in range(len(ls) - 1)]

    return list_or_tuple(res)


def unflat_len(obj):
    """Return number of non-list/tuple elements in obj."""
    if not isinstance(obj, (list, tuple)):
        return 1
    else:
        return sum([unflat_len(x) for x in obj])


def is_flat(obj):
    """Check whether list or tuple is flat, returns true if yes, false if nested."""
    return not any(isinstance(x, (list, tuple)) for x in obj)
