# -*- coding: utf-8 -*-
""":mod:`skbase.config` provides tools for the global configuration of ``skbase``.

For more information on configuration usage patterns see the
:ref:`user guide <user_guide_global_config>`.
"""
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Includes functionality like get_config, set_config, and config_context
# that is similar to scikit-learn. These elements are copyrighted by the
# scikit-learn developers, BSD-3-Clause License. For conditions see
# https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
from typing import List

from skbase.config._config import (
    GlobalConfigParamSetting,
    config_context,
    get_config,
    get_default_config,
    reset_config,
    set_config,
)

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = [
    "GlobalConfigParamSetting",
    "get_default_config",
    "get_config",
    "set_config",
    "reset_config",
    "config_context",
]
