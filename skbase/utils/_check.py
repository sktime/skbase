# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Elements of _is_scalar_nan reuse code developed in scikit-learn. These elements
# are copyrighted by the scikit-learn developers, BSD-3-Clause License. For
# conditions see https://github.com/scikit-learn/scikit-learn/blob/main/COPYING

"""Utility functions to perform various types of checks."""
from __future__ import annotations

import math
import numbers
from typing import Any

__all__ = ["_is_scalar_nan"]
__author__ = ["RNKuhns"]


def _is_scalar_nan(x: Any) -> bool:
    """Test if x is NaN.

    This function is meant to overcome the issue that np.isnan does not allow
    non-numerical types as input, and that np.nan is not float('nan').

    Parameters
    ----------
    x : Any
        The item to be checked to determine if it is a scalar nan value.

    Returns
    -------
    bool
        True if `x` is a scalar nan value

    Notes
    -----
    This code follows scikit-learn's implementation.

    Examples
    --------
    >>> import numpy as np
    >>> from skbase.utils._check import _is_scalar_nan
    >>> _is_scalar_nan(np.nan)
    True
    >>> _is_scalar_nan(float("nan"))
    True
    >>> _is_scalar_nan(None)
    False
    >>> _is_scalar_nan("")
    False
    >>> _is_scalar_nan([np.nan])
    False
    """
    return isinstance(x, numbers.Real) and math.isnan(x)
