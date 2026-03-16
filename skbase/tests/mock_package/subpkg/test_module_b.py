# -*- coding: utf-8 -*-
"""Module inside subpackage to test recursive discovery."""


def subpkg_fn():
    """Return the string "ok" to indicate functionality."""
    return "ok"


__all__ = ["subpkg_fn"]
