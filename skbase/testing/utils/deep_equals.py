# -*- coding: utf-8 -*-
"""Deprecation forwarding of equality checker utilities."""

# todo 0.6.0 - remove this forward

from warnings import warn

from skbase.utils import deep_equals

warn(
    "deep_equals has moved to "
    "skbase.utils.deep_equals. The old location will be removed in skbase 0.6.0."
)

__all__ = ["deep_equals"]
