# -*- coding: utf-8 -*-
# copyright: BaseObject developers, BSD-3-Clause License (see LICENSE file)
"""Custom exceptions used in ``baseobject``."""
from typing import List

__author__: List[str] = ["mloning", "rnkuhns"]
__all__: List[str] = ["NotFittedError"]


class NotFittedError(ValueError, AttributeError):
    """Exception class to raise if estimator is used before fitting.

    This class inherits from both ValueError and AttributeError to help with
    exception handling.

    References
    ----------
    [1] scikit-learn's NotFittedError
    [2] sktime's NotFittedError
    """
