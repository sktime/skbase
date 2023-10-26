# -*- coding: utf-8 -*-
"""Common utility functions for skbase.utils.deep_equals."""


def _ret(is_equal, msg="", string_arguments: list = None, return_msg=False):
    """Return is_equal and msg, formatted with string_arguments if return_msg=True.

    Parameters
    ----------
    is_equal : bool
    msg : str, optional, default=""
        message to return if is_equal=False
    string_arguments : list, optional, default=None
        list of arguments to format msg with

    Returns
    -------
    is_equal : bool
        identical to input ``is_equal``, always returned
    msg : str, only returned if return_msg=True
        if ``is_equal=True``, ``msg`` is always ``""``
        if ``is_equal=False``, ``msg`` is formatted with ``string_arguments``
        via ``msg.format(*string_arguments)``
    """
    if return_msg:
        if is_equal:
            msg = ""
        elif isinstance(string_arguments, (list, tuple)) and len(string_arguments) > 0:
            msg = msg.format(*string_arguments)
        return is_equal, msg
    else:
        return is_equal


def _make_ret(return_msg):
    """Curry _ret with return_msg."""

    def ret(is_equal, msg, string_arguments=None):
        return _ret(is_equal, msg, string_arguments, return_msg)

    return ret
