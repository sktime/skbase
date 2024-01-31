# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Validate if an input is one of the allowed named object formats."""
import collections.abc

from skbase.base import BaseObject

__all__ = [
    "check_sequence_named_objects",
    "is_named_object_tuple",
    "is_sequence_named_objects",
]
__author__ = ["RNKuhns"]


def _named_baseobject_error_msg(sequence_name=None, allow_dict=True):
    """Create error message for non-conformance with named BaseObject api."""
    name_str = f"{sequence_name}" if sequence_name is not None else "Input"
    allowed_types = "a sequence of (string name, BaseObject instance) tuples"

    if allow_dict:
        allowed_types += " or dict[str, BaseObject instance]"
    msg = f"Invalid {name_str!r}, {name_str!r} should be {allowed_types}."
    return msg


def is_named_object_tuple(obj, object_type=None):
    """Indicate if input is a a tuple of format (str, `object_type`).

    Used to validate that input follows named object tuple API format.

    Parameters
    ----------
    obj : Any
        The object to be checked to see if it is a (str, `object_type`) tuple.
    object_type : class or tuple of class, default=BaseObject
        Class(es) that all objects are checked to be an instance of. If None,
        then :class:``skbase.base.BaseObject`` is used as default.

    Returns
    -------
    bool
        True if obj is (str, `object_type`) tuple, otherwise False.

    See Also
    --------
    is_sequence_named_objects :
        Indicate (True/False) if an input sequence follows the named object API.
    check_sequence_named_objects :
        Validate input to see if it follows sequence of named objects API. An error
        is raised for input that does not conform to the API format.

    Examples
    --------
    >>> from skbase.base import BaseObject, BaseEstimator
    >>> from skbase.validate import is_named_object_tuple

    Default checks for object to be an instance of BaseObject

    >>> is_named_object_tuple(("Step 1", BaseObject()))
    True

    >>> is_named_object_tuple(("Step 2", BaseEstimator()))
    True

    If a different `object_type` is provided then it is used in the isinstance check

    >>> is_named_object_tuple(("Step 1", BaseObject()), object_type=BaseEstimator)
    False

    >>> is_named_object_tuple(("Step 1", BaseEstimator()), object_type=BaseEstimator)
    True

    If the input is does not follow named object tuple format then False is returned

    >>> is_named_object_tuple({"Step 1": BaseEstimator()})
    False

    >>> is_named_object_tuple((1, BaseObject()))
    False
    """
    if object_type is None:
        object_type = BaseObject
    if not isinstance(obj, tuple) or len(obj) != 2:
        return False
    if not isinstance(obj[0], str) or not isinstance(obj[1], object_type):
        return False
    return True


def is_sequence_named_objects(
    seq_to_check,
    allow_dict=True,
    require_unique_names=False,
    object_type=None,
):
    """Indicate if input is a sequence of named BaseObject instances.

    This can be a sequence of (str, BaseObject instance) tuples or
    a dictionary with string names as keys and BaseObject instances as values
    (if ``allow_dict=True``).

    Parameters
    ----------
    seq_to_check : Sequence((str, BaseObject)) or Dict[str, BaseObject]
        The input to check for conformance with the named object interface.
        Conforming input are:

        - Sequence that contains (str, BaseObject instance) tuples
        - Dictionary with string names as keys and BaseObject instances as values
          if ``allow_dict=True``

    allow_dict : bool, default=True
        Whether a dictionary of named objects is allowed as conforming named object
        type.

        - If True, then a dictionary with string keys and BaseObject instances
          is allowed format for providing a sequence of named objects.
        - If False, then only sequences that contain (str, BaseObject instance)
          tuples are considered conforming with the named object parameter API.

    require_unique_names : bool, default=False
        Whether names used in the sequence of named BaseObject instances
        must be unique.

        - If True and the names are not unique, then False is always returned.
        - If False, then whether or not the function returns True or False
          depends on whether `seq_to_check` follows sequence of named
          BaseObject format.

    object_type : class or tuple[class], default=None
        The class type(s) that is used to ensure that all elements of named objects
        match the expected type.

    Returns
    -------
    bool
        Whether the input `seq_to_check` is a sequence that follows the API for
        nameed base object instances.

    Raises
    ------
    ValueError
        If `seq_to_check` is not a sequence or ``allow_dict is False`` and
        `seq_to_check` is a dictionary.

    See Also
    --------
    is_named_object_tuple :
        Indicate (True/False) if input follows the named object API format for
        a single named object (e.g., tuple[str, expected class type]).
    check_sequence_named_objects :
        Validate input to see if it follows sequence of named objects API. An error
        is raised for input that does not conform to the API format.

    Examples
    --------
    >>> from skbase.base import BaseObject, BaseEstimator
    >>> from skbase.validate import is_sequence_named_objects
    >>> named_objects = [("Step 1", BaseObject()), ("Step 2", BaseObject())]
    >>> is_sequence_named_objects(named_objects)
    True

    Dictionaries are optionally allowed as sequences of named BaseObjects

    >>> dict_named_objects = {"Step 1": BaseObject(), "Step 2": BaseObject()}
    >>> is_sequence_named_objects(dict_named_objects)
    True
    >>> is_sequence_named_objects(dict_named_objects, allow_dict=False)
    False

    Invalid format due to object names not being strings

    >>> incorrectly_named_objects = [(1, BaseObject()), (2, BaseObject())]
    >>> is_sequence_named_objects(incorrectly_named_objects)
    False

    Invalid format due to named items not being BaseObject instances

    >>> named_items = [("1", 7), ("2", 42)]
    >>> is_sequence_named_objects(named_items)
    False

    The validation can require the object elements to be a certain class type

    >>> named_objects = [("Step 1", BaseObject()), ("Step 2", BaseObject())]
    >>> is_sequence_named_objects(named_objects, object_type=BaseEstimator)
    False
    >>> named_objects = [("Step 1", BaseEstimator()), ("Step 2", BaseEstimator())]
    >>> is_sequence_named_objects(named_objects, object_type=BaseEstimator)
    True
    """
    # Want to end quickly if the input isn't sequence or is a dict and we
    # aren't allowing dicts
    if object_type is None:
        object_type = BaseObject

    is_dict = isinstance(seq_to_check, dict)
    if (not is_dict and not isinstance(seq_to_check, collections.abc.Sequence)) or (
        not allow_dict and is_dict
    ):
        return False

    if is_dict:
        elements_expected_format = [
            isinstance(name, str) and isinstance(obj, object_type)
            for name, obj in seq_to_check.items()
        ]
        all_unique_names = True
    else:
        names = []
        elements_expected_format = []
        for it in seq_to_check:
            if is_named_object_tuple(it, object_type=object_type):
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


def check_sequence_named_objects(
    seq_to_check,
    allow_dict=True,
    require_unique_names=False,
    object_type=None,
    sequence_name=None,
):
    """Check if input is a sequence of named BaseObject instances.

    `seq_to_check` is returned unchanged when it follows the allowed named
    BaseObject convention. The allowed format includes a sequence of
    (str, BaseObject instance) tuples. A dictionary with string names as keys
    and BaseObject instances as values is also allowed if ``allow_dict is True``.

    Parameters
    ----------
    seq_to_check : Sequence((str, BaseObject)) or Dict[str, BaseObject]
        The input to check for conformance with the named object interface.
        Conforming input are:

        - Sequence that contains (str, BaseObject instance) tuples
        - Dictionary with string names as keys and BaseObject instances as values
          if ``allow_dict=True``

    allow_dict : bool, default=True
        Whether a dictionary of named objects is allowed as conforming named object
        type.

        - If True, then a dictionary with string keys and BaseObject instances
          is allowed format for providing a sequence of named objects.
        - If False, then only sequences that contain (str, BaseObject instance)
          tuples are considered conforming with the named object parameter API.

    require_unique_names : bool, default=False
        Whether names used in the sequence of named BaseObject instances
        must be unique.

        - If True and the names are not unique, then False is always returned.
        - If False, then whether or not the function returns True or False
          depends on whether `seq_to_check` follows sequence of named BaseObject format.

    object_type : class or tuple[class], default=None
        The class type(s) that is used to ensure that all elements of named objects
        match the expected type.
    sequence_name : str, default=None
        Optional name used to refer to the input `seq_to_check` when
        raising any errors. Ignored ``raise_error=False``.

    Returns
    -------
    Sequence((str, BaseObject)) or Dict[str, BaseObject]
        The `seq_to_check` is returned if it is a conforming named object type.

        - If ``allow_dict=True`` then return type is Sequence((str, BaseObject))
          or Dict[str, BaseObject]
        - If ``allow_dict=False`` then return type is Sequence((str, BaseObject))

    Raises
    ------
    ValueError
        If `seq_to_check` does not conform to the named BaseObject API.

    See Also
    --------
    is_named_object_tuple :
        Indicate (True/False) if input follows the named object API format for
        a single named object (e.g., tuple[str, expected class type]).
    is_sequence_named_objects :
        Indicate (True/False) if an input sequence follows the named object API.

    Examples
    --------
    >>> from skbase.base import BaseObject, BaseEstimator
    >>> from skbase.validate import check_sequence_named_objects
    >>> named_objects = [("Step 1", BaseObject()), ("Step 2", BaseObject())]
    >>> check_sequence_named_objects(named_objects)
    [('Step 1', BaseObject()), ('Step 2', BaseObject())]

    Dictionaries are optionally allowed as sequences of named BaseObjects

    >>> named_objects = {"Step 1": BaseObject(), "Step 2": BaseObject()}
    >>> check_sequence_named_objects(named_objects)
    {'Step 1': BaseObject(), 'Step 2': BaseObject()}

    Raises error since dictionaries are not allowed when allow_dict is False

    >>> check_sequence_named_objects(named_objects, allow_dict=False) # doctest: +SKIP

    Raises error due to invalid format due to object names not being strings

    >>> incorrectly_named_objects = [(1, BaseObject()), (2, BaseObject())]
    >>> check_sequence_named_objects(incorrectly_named_objects)  # doctest: +SKIP

    Raises error due to invalid format since named items are not BaseObject instances

    >>> named_items = [("1", 7), ("2", 42)]
    >>> check_sequence_named_objects(named_items)  # doctest: +SKIP

    The validation can require the object elements to be a certain class type

    >>> named_objects = [("Step 1", BaseObject()), ("Step 2", BaseObject())]
    >>> check_sequence_named_objects( \
    named_objects, object_type=BaseEstimator) # doctest: +SKIP
    >>> named_objects = [("Step 1", BaseEstimator()), ("Step 2", BaseEstimator())]
    >>> check_sequence_named_objects(named_objects, object_type=BaseEstimator)
    [('Step 1', BaseEstimator()), ('Step 2', BaseEstimator())]
    """
    is_expected_format = is_sequence_named_objects(
        seq_to_check,
        allow_dict=allow_dict,
        require_unique_names=require_unique_names,
        object_type=object_type,
    )
    # Raise error is format is not expected.
    if not is_expected_format:
        msg = _named_baseobject_error_msg(
            sequence_name=sequence_name, allow_dict=allow_dict
        )
        raise ValueError(msg)

    return seq_to_check
