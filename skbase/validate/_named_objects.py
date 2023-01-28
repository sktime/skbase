# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Validate if an input is one of the allowed named object formats."""
import collections.abc
from typing import Dict, Iterable, List, Optional, Tuple, Union, overload

from skbase.base import BaseObject

__all__: List[str] = ["check_iterable_named_objects", "is_iterable_named_objects"]
__author__: List[str] = ["RNKuhns"]


def _named_baseobject_error_msg(
    iterable_name: Optional[str] = None, allow_dict: bool = True
):
    """Create error message for non-comformance with named BaseObject api."""
    name_str = f"{iterable_name}" if iterable_name is not None else "Input"
    allowed_types = "an iterable of (string name, BaseObject instance) tuples"

    if allow_dict:
        allowed_types += " or dict[str, BaseObject instance]"
    msg = f"Invalid '{name_str}', '{name_str}' should be {allowed_types}."
    return msg


@overload
def is_iterable_named_objects(
    iterable_to_check: Iterable[Tuple[str, BaseObject]],
    allow_dict: bool = False,
    require_unique_names=False,
) -> bool:
    ...


@overload
def is_iterable_named_objects(
    iterable_to_check: Union[Iterable[Tuple[str, BaseObject]], Dict[str, BaseObject]],
    allow_dict: bool = True,
    require_unique_names=False,
) -> bool:
    ...


def is_iterable_named_objects(
    iterable_to_check: Union[Iterable[Tuple[str, BaseObject]], Dict[str, BaseObject]],
    allow_dict: bool = True,
    require_unique_names=False,
) -> bool:
    """Indicate if input is an iterable of named BaseObject instances.

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
        Whether a dictionary of named objects is allowed as conforming named object
        type.

        - If True, then a dictionary with string keys and BaseObject instances
          is allowed format for providing an iterable of named objects.
        - If False, then only iterables that contain (str, BaseObject instance)
          tuples are considered conforming with the named object parameter API.

    iterable_name : str, default=None
        Optional name used to refer to the input `iterable_to_check` when
        raising any errors.

    Returns
    -------
    iterable_to_check : Iterable((str, BaseObject)) or Dict[str, BaseObject]
        The `iterable_to_check` is returned if it is a conforming named object type.

    Raises
    ------
    ValueError
        If `iterable_to_check` is not an iterable or ``allow_dict is False`` and
        `iterable_to_check` is a dictionary.

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
    >>> is_iterable_named_objects(dict_named_objects, allow_dict=False)
    False

    # Invalid format due to object names not being strings
    >>> iterable_incorrectly_named_objects = [(1, BaseObject()), (2, BaseObject())]
    >>> is_iterable_named_objects(iterable_incorrectly_named_objects)
    False

    # Invalid format due to named items not being BaseObject instances
    >>> iterable_named_items = [("1", 7), ("2", 42)]
    >>> is_iterable_named_objects(iterable_named_items)
    False
    """
    # Want to end quickly if the input isn't iterable or is a dict and we
    # aren't allowing dicts
    if not isinstance(iterable_to_check, collections.abc.Iterable) or (
        isinstance(iterable_to_check, dict) and not allow_dict
    ):
        is_expected_format = False
        return is_expected_format

    all_expected_format: bool
    all_unique_names: bool
    if isinstance(iterable_to_check, dict):
        elements_expected_format = [
            isinstance(name, str) and isinstance(obj, BaseObject)
            for name, obj in iterable_to_check.items()
        ]
        all_unique_names = True
    else:
        names = []
        elements_expected_format = []
        for it in iterable_to_check:
            if (
                isinstance(it, tuple)
                and len(it) == 2
                and (isinstance(it[0], str) and isinstance(it[1], BaseObject))
            ):
                elements_expected_format.append(True)
                names.append(it[0])
            else:
                elements_expected_format.append(False)
        all_unique_names = len(set(names)) == len(names)

    all_expected_format = all(elements_expected_format)

    if not all_expected_format or (require_unique_names and not all_unique_names):
        is_expected_format = False
    else:
        is_expected_format = True

    return is_expected_format


@overload
def check_iterable_named_objects(
    iterable_to_check: Iterable[Tuple[str, BaseObject]],
    allow_dict: bool = False,
    require_unique_names=False,
    iterable_name: Optional[str] = None,
) -> Iterable[Tuple[str, BaseObject]]:
    ...


@overload
def check_iterable_named_objects(
    iterable_to_check: Union[Iterable[Tuple[str, BaseObject]], Dict[str, BaseObject]],
    allow_dict: bool = True,
    require_unique_names=False,
    iterable_name: Optional[str] = None,
) -> Union[Iterable[Tuple[str, BaseObject]], Dict[str, BaseObject]]:
    ...


def check_iterable_named_objects(
    iterable_to_check: Union[Iterable[Tuple[str, BaseObject]], Dict[str, BaseObject]],
    allow_dict: bool = True,
    require_unique_names=False,
    iterable_name: Optional[str] = None,
) -> Union[Iterable[Tuple[str, BaseObject]], Dict[str, BaseObject]]:
    """Check if input is an iterable of named BaseObject instances.

    `iterable_to_check` is returned unchanged when it follows the allowed named
    BaseObject format. The allowed format includes iterable of
    (str, BaseObject instance) tuples. A dictionary with string names as keys
    and BaseObject instances as values is also allowed if ``allow_dict is True``.

    Parameters
    ----------
    iterable_to_check : Iterable((str, BaseObject)) or Dict[str, BaseObject]
        The iterable to check for conformance with the named object interface.
        Conforming iterables are:

        - Iterable that contains (str, BaseObject instance) tuples
        - Dictionary with string names as keys and BaseObject instances as values
            if ``allow_dict=True``

    allow_dict : bool, default=True
        Whether a dictionary of named objects is allowed as conforming named object
        type.

        - If True, then a dictionary with string keys and BaseObject instances
          is allowed format for providing an iterable of named objects.
        - If False, then only iterables that contain (str, BaseObject instance)
          tuples are considered conforming with the named object parameter API.

    require_unique_names : bool, default=False
        Whether names used in the iterable of named BaseObject instances
        must be unique.

        - If True and the names are not unique, then False is always returned.
        - If False, then whether or not the function returns True or False
          depends on whether `iterable_to_check` follows iterable of named
          BaseObject format.

    iterable_name : str, default=None
        Optional name used to refer to the input `iterable_to_check` when
        raising any errors. Ignored ``raise_error=False``.

    Returns
    -------
    iterable_to_check : Iterable((str, BaseObject)) or Dict[str, BaseObject]
        The `iterable_to_check` is returned if it is a conforming named object type.

    Raises
    ------
    ValueError
        If `iterable_to_check` does not conform to the named BaseObject API.

    Examples
    --------
    >>> from skbase.base import BaseObject
    >>> from skbase.validate import check_iterable_named_objects
    >>> iterable_of_named_objects = [("Step 1", BaseObject()), ("Step 2", BaseObject())]
    >>> check_iterable_named_objects(iterable_of_named_objects)
    [('Step 1', BaseObject()), ('Step 2', BaseObject())]

    >>> dict_named_objects = {"Step 1": BaseObject(), "Step 2": BaseObject()}
    >>> check_iterable_named_objects(dict_named_objects)
    {'Step 1': BaseObject(), 'Step 2': BaseObject()}

    # Raises error since dictionaries are not allowed when allow_dict is False
    >>> check_iterable_named_objects(dict_named_objects, \
    allow_dict=False) # doctest: +SKIP

    # Raises error due to invalid format due to object names not being strings
    >>> incorrectly_named_objects = [(1, BaseObject()), (2, BaseObject())]
    >>> check_iterable_named_objects(incorrectly_named_objects)  # doctest: +SKIP

    # Raises error due to invalid format since named items are not BaseObject instances
    >>> iterable_named_items = [("1", 7), ("2", 42)]
    >>> check_iterable_named_objects(iterable_named_items)  # doctest: +SKIP
    """
    is_expected_format = is_iterable_named_objects(
        iterable_to_check,
        allow_dict=allow_dict,
        require_unique_names=require_unique_names,
    )
    # Raise error is format is not expected.
    if not is_expected_format:
        msg = _named_baseobject_error_msg(
            iterable_name=iterable_name, allow_dict=allow_dict
        )
        raise ValueError(msg)

    return iterable_to_check
