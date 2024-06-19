# -*- coding: utf-8 -*-
"""Context manager to suppress stdout."""

__author__ = ["fkiraly"]

import io
import sys
import warnings


class StdoutMute:
    """A context manager to suppress stdout.

    This class is used to suppress stdout when importing modules.

    Also downgrades any ModuleNotFoundError to a warning if the error message
    contains the substring "soft dependency".

    Parameters
    ----------
    active : bool, default=True
        Whether to suppress stdout or not.
        If True, stdout is suppressed.
        If False, stdout is not suppressed, and the context manager does nothing
        except catch and suppress ModuleNotFoundError.
    """

    def __init__(self, active=True):
        self.active = active

    def __enter__(self):
        """Context manager entry point."""
        # capture stdout if active
        # store the original stdout so it can be restored in __exit__
        if self.active:
            self._stdout = sys.stdout
            sys.stdout = io.StringIO()

    def __exit__(self, type, value, traceback):  # noqa: A002
        """Context manager exit point."""
        # restore stdout if active
        # if not active, nothing needs to be done, since stdout was not replaced
        if self.active:
            sys.stdout = self._stdout

        if type is not None:
            # if a ModuleNotFoundError is raised,
            # we suppress to a warning if "soft dependency" is in the error message
            # otherwise, raise
            if type is ModuleNotFoundError:
                if "soft dependency" not in str(value):
                    return False
                warnings.warn(str(value), ImportWarning, stacklevel=2)
                return True

            # all other exceptions are raised
            return False
        # if no exception was raised, return True to indicate successful exit
        # return statement not needed as type was None, but included for clarity
        return True
