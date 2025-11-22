# -*- coding: utf-8 -*-
"""Non-public module in mock package; contains a non-public BaseObject subclass.

This module's class name begins with an underscore and should be ignored by
`all_objects` when `exclude_non_public_items` is True.
"""

from skbase.base import BaseObject


class _PrivateThing(BaseObject):
    """A non-public BaseObject subclass that should be ignored by discovery."""

    def __init__(self):
        super().__init__()


__all__ = ["_PrivateThing"]
