# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for skbase pretty printing functionality."""

import pytest

from skbase.base import BaseObject
from skbase.utils.dependencies import _check_soft_dependencies


class CompositionDummy(BaseObject):
    """Potentially composite object, for testing."""

    def __init__(self, foo, bar=84):
        self.foo = foo
        self.bar = bar

        super(CompositionDummy, self).__init__()


@pytest.mark.skipif(
    not _check_soft_dependencies("scikit-learn", severity="none"),
    reason="skip test if sklearn is not available",
)  # sklearn is part of the dev dependency set, test should be executed with that
def test_sklearn_compatibility():
    """Test that the pretty printing functions are compatible with sklearn."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.pipeline import make_pipeline

    regressor = make_pipeline(
        RandomForestRegressor(),
    )
    CompositionDummy(regressor)
