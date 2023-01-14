# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Validate if an input is one of the allowed named object formats."""
import collections.abc
from typing import Dict, Iterable, List, Optional, Tuple, Union, overload

from skbase.base import BaseObject

__all__: List[str] = ["is_iterable_named_objects"]
__author__: List[str] = ["RNKuhns"]


@overload
def is_iterable_named_objects(
    iterable_to_check: Iterable[Tuple[str, BaseObject]],
    allow_dict: bool = False,
    raise_error: bool = True,
    iterable_name: Optional[str] = None,
) -> Optional[bool]:
    ...


@overload
def is_iterable_named_objects(
    iterable_to_check: Union[Iterable[Tuple[str, BaseObject]], Dict[str, BaseObject]],
    allow_dict: bool = True,
    raise_error: bool = True,
    iterable_name: Optional[str] = None,
) -> Optional[bool]:
    ...


def is_iterable_named_objects(
    iterable_to_check: Union[Iterable[Tuple[str, BaseObject]], Dict[str, BaseObject]],
    allow_dict: bool = True,
    raise_error: bool = True,
    iterable_name: Optional[str] = None,
) -> Optional[bool]:
    """Check if input is an iterable of named BaseObject instances.

    This can be an iterable of (str, BaseObject instance) tuples or
    a dictionary with string names as keys and BaseObject instances as values
    (if ``allow_dict=True``).

    Parameters
    ----------
    iterable_to_check : Iterable((str, BaseObject)) or Dict[str, BaseObject]
        The iterable to check for conformance with the named object interface.
        Conforming iterables are:

        - Iterable that contains (str, BaseObject instance) tuples
        - Dictionary with string names as keys and BaseObject instances as values
            if ``allow_dict=True``

    allow_dict : bool, default=True
        Whether a dictionary with string names as keys and BaseObject instances
        is an allowed format for providing a iterable of named objects.
        If False, then only iterables that contain (str, BaseObject instance)
        tuples are considered conforming with the named object parameter API.
    raise_error : bool, default=True
        Whether an error should be raised for non-conforming input. If True,
        an error is raised. If False, then True is returned when
        `iterable_to_check` conforms to expected format and False is returned
        when it is non-confomring.
    iterable_name : str, default=None
        Optional name used to refer to the input `iterable_to_check` when
        raising any errors. Ignored ``raise_error=False``.

    Returns
    -------
    is_named_object_input : bool
        If True, then `iterable_to_check` follows the expected named object
        parameter API.

    Raises
    ------
    ValueError
        If `iterable_to_check` is not an iterable or it does not conform
        to the named BaseObject API (e.g., it has non-unique name elements or
        does not follow required formatting conventions).

    Examples
    --------
    >>> from skbase.base import BaseObject
    >>> from skbase.validate import is_iterable_named_objects
    >>> iterable_of_named_objects = [("Step 1", BaseObject()), ("Step 2", BaseObject())]
    >>> is_iterable_named_objects(iterable_of_named_objects)
    True

    >>> dict_named_objects = {"Step 1": BaseObject(), "Step 2": BaseObject()}
    >>> is_iterable_named_objects(dict_named_objects)
    True
    >>> is_iterable_named_objects(dict_named_objects, allow_dict=False, \
    raise_error=False)
    False
    >>> is_iterable_named_objects(dict_named_objects, allow_dict=False) # doctest: +SKIP

    # Invalid format due to object names not being strings
    >>> iterable_incorrectly_named_objects = [(1, BaseObject()), (2, BaseObject())]
    >>> is_iterable_named_objects(iterable_incorrectly_named_objects, raise_error=False)
    False

    # Invalid format due to named items not being BaseObject instances
    >>> iterable_named_items = [("1", 7), ("2", 42)]
    >>> is_iterable_named_objects(iterable_named_items, raise_error=False)
    False
    """
    name_str = f"Input {iterable_name}" if iterable_name is not None else "Input"
    # Want to end quickly if the input isn't iterable
    if not isinstance(iterable_to_check, collections.abc.Iterable):
        if raise_error:
            raise ValueError(f"{name_str} is not iterable.")
        else:
            return False

    names: List[str]
    all_unique_names: bool
    if isinstance(iterable_to_check, dict):
        if allow_dict:
            is_expected_format = [
                isinstance(name, str) and isinstance(obj, BaseObject)
                for name, obj in iterable_to_check.items()
            ]
            names = [*iterable_to_check.keys()]
            all_unique_names = True
        else:
            if isinstance(iterable_to_check, dict):
                if raise_error:
                    raise ValueError(
                        "Input is a dictionary, but dictionaries are only allowed as "
                        "as input when checking for iterables of named objects "
                        "using function `is_iterable_named_objects` "
                        "when ``allow_dict=True``."
                    )
                else:
                    return False
    else:
        is_expected_format = [
            isinstance(it, tuple)
            and len(it) == 2
            and (isinstance(it[0], str) and isinstance(it[1], BaseObject))
            for it in iterable_to_check
        ]
        names = [it[0] for it in iterable_to_check]
        all_unique_names = len(set(names)) == len(names)

    all_expected_format: bool = all(is_expected_format)
    not_expected_format = [
        item
        for item, is_type in zip(iterable_to_check, is_expected_format)
        if not is_type
    ]
    non_unique_names: List[str] = []
    if not all_unique_names:
        name_count = collections.Counter(iterable_to_check)
        non_unique_names = [c for c in name_count if name_count[c] > 1]

    if raise_error and not (all_expected_format and all_unique_names):
        if all_unique_names:
            non_unique_str = ""
        else:
            non_unique_str = (
                f"{name_str} has non unique name elements: " f"{non_unique_names}."
            )
        if all_expected_format:
            not_exp_format_str = ""
        else:
            expected_format = "an iterable of (string name, BaseObject instance) tuples"
            if allow_dict:
                expected_format = expected_format + " or Dict[str, BaseObject instance]"
            not_exp_format_str = (
                f"{name_str} has items that do not match expected iterable of named "
                f"objects format of {expected_format}: {not_expected_format}."
            )
        if not all_expected_format or not all_unique_names:
            raise ValueError(
                f"{name_str} does not conform to the expected "
                "named base object API.\n"
                f"{not_exp_format_str}\n{non_unique_str}"
            )

    return all_expected_format and all_unique_names
