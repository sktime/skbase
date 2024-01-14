# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tests of random_seed related functionality."""
import pytest

from skbase.utils.random_state import sample_dependent_seed, set_random_state

__author__ = ["fkiraly"]


@pytest.mark.parametrize("seed", [1, 42, "foo"])
@pytest.mark.parametrize("n_seeds", [None, 0, 1, 12])
def test_sample_dependent_seed(seed, n_seeds):
    """Test sample_dependent_seed returns expected output type."""
    seeds = sample_dependent_seed(seed=seed, n_seeds=n_seeds)

    if n_seeds is None:
        assert isinstance(seeds, int)
    else:
        assert isinstance(seeds, list)
        assert len(seeds) == n_seeds
        assert all(isinstance(s, int) for s in seeds)


@pytest.mark.parametrize("deep", [True, False])
@pytest.mark.parametrize("external", [True, False])
def test_set_random_state(external, deep):
    """Test _format_seq_to_str returns expected output."""
    # importing here to avoid circularity
    from skbase.base import BaseObject

    def set_seed(obj):
        if external:
            return set_random_state(obj, seed=42, deep=deep)
        else:
            return obj.set_random_state(seed=42, deep=deep)

    class DummyDummy(BaseObject):
        """Has no random_state attribute."""

        def __init__(self, foo):
            self.foo = foo

            super(DummyDummy, self).__init__()

    class SeedCompositionDummy(BaseObject):
        """Potentially composite object, for testing."""

        def __init__(self, foo, random_state=None):
            self.foo = foo
            self.random_state = random_state

            super(SeedCompositionDummy, self).__init__()

    simple = SeedCompositionDummy(foo=1, random_state=42)
    seedless = DummyDummy(foo=42)
    composite1 = SeedCompositionDummy(foo=simple, random_state=42)
    composite2 = SeedCompositionDummy(foo=seedless, random_state=None)

    # in the simple case, the seed is set
    # even though the seed in set_random_seed is 42, the set param will not be 42,
    # because it is sampled from the set_random_seed seed 42
    set_seed(simple)
    assert simple.get_params()["random_state"] != 42

    # this does not have a random_state attribute
    # all we test is that it does not break
    set_seed(seedless)

    # in the composite case, the seed is set
    # what happens to the nested param depends on the deep argument
    set_seed(composite1)
    assert composite1.get_params()["random_state"] != 42
    if deep:
        assert composite1.get_params()["foo__random_state"] != 42
    else:
        assert composite1.get_params()["foo__random_state"] == 42

    # here we test two things:
    # does not break for seedless composites
    # behaviour if self.random_state is None
    set_seed(composite2)
    assert composite2.get_params()["random_state"] is not None
    assert composite2.get_params()["random_state"] != 42
