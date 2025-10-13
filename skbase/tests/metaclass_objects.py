# -*- coding: utf-8 -*-
"""Metaclass-based fixtures for lookup tests."""

from typing import List

from skbase.utils.dependencies._import import CommonMagicMeta

__all__: List[str] = ["MetaExample", "MetaSubclass"]
__author__: List[str] = ["skbase developers"]


class MetaExample(metaclass=CommonMagicMeta):
    """Minimal class using CommonMagicMeta for lookup regression tests."""


class MetaSubclass(MetaExample):
    """Subclass of MetaExample to ensure derived classes remain discoverable."""
