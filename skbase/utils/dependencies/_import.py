# -*- coding: utf-8 -*-
"""Utility for safe import."""
import importlib


def _safe_import(path, condition=True):
    """Safely imports an object from a module given its string location.

    Parameters
    ----------
    path: str
        A string representing the module and object.
        In the form ``"module.submodule:object"``.
    condition: bool, default=True
        If False, the import will not be attempted.

    Returns
    -------
    Any: The imported object, or None if it could not be imported.
    """
    if not condition:
        return None
    try:
        module_name, object_name = path.split(":")
        module = importlib.import_module(module_name)
        return getattr(module, object_name, None)
    except (ImportError, AttributeError, ValueError):
        return None
