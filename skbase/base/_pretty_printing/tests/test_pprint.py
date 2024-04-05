# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests for skbase pretty printing functionality."""

from skbase.base import BaseObject


class CompositionDummy(BaseObject):
    """Potentially composite object, for testing."""

    def __init__(self, foo, bar=84):
        self.foo = foo
        self.bar = bar

        super(CompositionDummy, self).__init__()


def test_sklearn_compatibility():
    """Test that the pretty printing functions are compatible with sklearn."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.pipeline import make_pipeline

    regressor = make_pipeline(
        RandomForestRegressor(),
    )
    CompositionDummy(regressor)
