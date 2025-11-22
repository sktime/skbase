# -*- coding: utf-8 -*-
"""Module inside subpackage to test recursive discovery."""


def subpkg_fn():
    """Simple function in subpackage module."""
    return "ok"


__all__ = ["subpkg_fn"]
