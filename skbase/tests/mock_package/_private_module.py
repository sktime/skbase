# -*- coding: utf-8 -*-
"""Private module in mock package for lookup non-public coverage."""

from skbase.base import BaseObject


class PrivateModuleClass(BaseObject):
    """Publicly named class living in a private module."""


class _PrivateModuleHiddenClass(BaseObject):
    """Non-public class living in a private module."""


def private_module_public_function():
    """Function with public name in a private module."""
    return "visible-only-when-non-public-modules-included"


def _private_module_hidden_function():
    """Function with private name in a private module."""
    return "visible-only-when-non-public-items-included"


__all__ = [
    "PrivateModuleClass",
    "_PrivateModuleHiddenClass",
    "private_module_public_function",
    "_private_module_hidden_function",
]
