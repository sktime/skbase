"""Tests for hybridmethod decorator."""

from inspect import isclass

from skbase.utils._hybridmethod import hybridmethod


class HybridmethodTestclass:

    def __init__(self):
        self.ref_to_self = self

    @hybridmethod
    def method(self_or_cls):

        if isclass(self_or_cls):
            assert self_or_cls is self_or_cls.ref_to_self
        else:
            assert self_or_cls is self_or_cls.ref_to_self
            assert isinstance(self_or_cls, self_or_cls.__class__)


HybridmethodTestclass.ref_to_self = HybridmethodTestclass


def test_hybridmethod():
    """Test that hybridmethod works as expected."""
    HybridmethodTestclass.method()
    HybridmethodTestclass().method()
