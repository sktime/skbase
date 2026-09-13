"""Tests for hybridmethod decorator."""

from inspect import isclass

from skbase.utils._hybridmethod import hybridmethod


class HybridmethodTestclass:

    def __init__(self):
        self.ref_to_self = self

    @hybridmethod
    def method(self):

        if isclass(self):
            assert self is self.ref_to_self
        else:
            assert self is self.ref_to_self
            assert isinstance(self, self.__class__)


HybridmethodTestclass.ref_to_self = HybridmethodTestclass


def test_hybridmethod():
    """Test that hybridmethod works as expected."""
    HybridmethodTestclass.method()
    HybridmethodTestclass().method()
