# -*- coding: utf-8 -*-
"""Class to hold information on a configurable parameter setting."""
import collections
import warnings
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, Union

from skbase.utils._iter import _format_seq_to_str

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = ["GlobalConfigParamSetting"]


@dataclass
class GlobalConfigParamSetting:
    """Define types of the setting information for a given config parameter."""

    name: str
    expected_type: Union[type, Tuple[type]]
    allowed_values: Optional[Union[Tuple[Any, ...], List[Any]]]
    default_value: Any

    def get_allowed_values(self) -> List[Any]:
        """Get `allowed_values` or empty tuple if `allowed_values` is None.

        Returns
        -------
        tuple
            Allowable values if any.
        """
        if self.allowed_values is None:
            return []
        elif isinstance(
            self.allowed_values, collections.abc.Iterable
        ) and not isinstance(self.allowed_values, str):
            return list(self.allowed_values)
        else:
            return [self.allowed_values]

    def is_valid_param_value(self, value):
        """Validate that a global configuration value is valid.

        Verifies that the value set for a global configuration parameter is valid
        based on the its configuration settings.

        Returns
        -------
        bool
            Whether a parameter value is valid.
        """
        allowed_values = self.get_allowed_values()

        valid_param: bool
        if not isinstance(value, self.expected_type):
            valid_param = False
        elif allowed_values is not None and value not in allowed_values:
            valid_param = False
        else:
            valid_param = True
        return valid_param

    def get_valid_param_or_default(self, value, default_value=None, msg=None):
        """Validate `value` and return default if it is not valid.

        Parameters
        ----------
        value : Any
            The configuration parameter value to set.
        default_value : Any, default=None
            An optional default value to use to set the configuration parameter
            if `value` is not valid based on defined expected type and allowed
            values. If None, and `value` is invalid then the classes `default_value`
            parameter is used.
        msg : str, default=None
            An optional message to be used as start of the UserWarning message.
        """
        if self.is_valid_param_value(value):
            return value
        else:
            if msg is None:
                msg = ""
            msg += f"When setting global config values for `{self.name}`, the values "
            msg += f"should be of type {self.expected_type}.\n"
            if self.allowed_values is not None:
                values_str = _format_seq_to_str(
                    self.get_allowed_values(), last_sep="or", remove_type_text=True
                )
                msg += f"Allowed values should be one of {values_str}. "
            msg += f"But found {value}."
            warnings.warn(msg, UserWarning, stacklevel=2)
            return default_value if default_value is not None else self.default_value
