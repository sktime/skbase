# -*- coding: utf-8 -*-
"""Deprecation forwarding of dependency checker utilities."""

# todo 0.6.0 - remove this forward

from warnings import warn

from skbase.utils.dependencies import _check_python_version, _check_soft_dependencies

warn(
    "_check_soft_dependencies, _check_python_versiontesting have moved to "
    "skbase.utils.dependencies. The old location will be removed in skbase 0.6.0."
)

__all__ = ["_check_python_version", "_check_soft_dependencies"]
