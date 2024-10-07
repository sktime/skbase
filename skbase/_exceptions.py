# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# NotFittedError reuse code developed in scikit-learn. These elements
# are copyrighted by the scikit-learn developers, BSD-3-Clause License. For
# conditions see https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
"""Custom exceptions used in ``skbase``."""
from typing import List

__author__: List[str] = ["fkiraly", "mloning", "rnkuhns"]
__all__: List[str] = ["FixtureGenerationError", "NotFittedError"]


class FixtureGenerationError(Exception):
    """Raised when a fixture fails to generate."""

    def __init__(self, fixture_name="", err=None):
        self.fixture_name = fixture_name
        super().__init__(f"fixture {fixture_name} failed to generate. {err}")


class NotFittedError(ValueError, AttributeError):
    """Exception class to raise if estimator is used before fitting.

    This class inherits from both ``ValueError`` and ``AttributeError`` to help with
    exception handling.

    References
    ----------
    .. [1] Based on scikit-learn's NotFittedError
    """
