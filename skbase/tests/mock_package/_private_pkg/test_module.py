# -*- coding: utf-8 -*-
"""Private module in mock package for non-public lookup coverage."""

from skbase.base import BaseObject


class PrivateModuleClass(BaseObject):
    """Represent a publicly named class in a private module."""


class _PrivateModuleHiddenClass(BaseObject):
    """Represent a non-public class in a private module."""


def private_module_public_function():
    """Return marker for a public function in a private module."""
    return "visible-only-when-non-public-modules-included"


def _private_module_hidden_function():
    """Return marker for a private function in a private module."""
    return "visible-only-when-non-public-items-included"


__all__ = [
    "PrivateModuleClass",
    "_PrivateModuleHiddenClass",
    "private_module_public_function",
    "_private_module_hidden_function",
]
