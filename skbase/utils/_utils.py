#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Functionality for working with sequences."""
from typing import Any, Iterable, List, MutableMapping, Optional, Union

__author__: List[str] = ["RNKuhns"]
__all__: List[str] = ["subset_dict_keys"]


def subset_dict_keys(
    input_dict: MutableMapping[Any, Any],
    keys: Union[Iterable, int, float, bool, str, type],
    prefix: Optional[str] = None,
    remove_prefix: bool = True,
):
    """Subset dictionary so it only contains specified keys.

    Subsets `input_dict` so that it only contains `keys`. If `prefix` is passed,
    subsets to `f"{prefix}__{key}"` for all `key` in `keys`. When
    ``remove_prefix=True`` the the prefix is removed from the keys of the
    return dictionary (For any keys with prefix the return is `{key}` instead
    of `f"{prefix}__{key}"`).

    Parameters
    ----------
    input_dict : dict
        Dictionary to subset by keys
    keys : iterable, int, float, bool, str or type
        The keys that should be retained in the output dictionary.
    prefix : str, default=None
        An optional prefix that is added to all keys. If `prefix` is passed,
        the passed keys are converted to `f"{prefix}__{key}"` when subsetting
        the dictionary. Results in all keys being coerced to str.
    remove_prefix : bool, default=True
        Whether to remove prefix in output keys.

    Returns
    -------
    `subsetted_dict` : dict
        `dict_to_subset` subset to keys in `keys` described as above

    Notes
    -----
    Passing `prefix` will turn non-str keys into str keys.

    Examples
    --------
    >>> from skbase.utils import subset_dict_keys
    >>> some_dict = {"some_param__a": 1, "some_param__b": 2, "some_param__c": 3}

    >>> subset_dict_keys(some_dict, "some_param__a")
    {'some_param__a': 1}

    >>> subset_dict_keys(some_dict, ("some_param__a", "some_param__b"))
    {'some_param__a': 1, 'some_param__b': 2}

    >>> subset_dict_keys(some_dict, ("a", "b"), prefix="some_param")
    {'a': 1, 'b': 2}

    >>> subset_dict_keys(some_dict, ("a", "b"), prefix="some_param", \
    remove_prefix=False)
    {'some_param__a': 1, 'some_param__b': 2}

    >>> subset_dict_keys(some_dict, \
    (c for c in ("some_param__a", "some_param__b")))
    {'some_param__a': 1, 'some_param__b': 2}
    """

    def rem_prefix(x):
        if not remove_prefix or prefix is None:
            return x
        prefix__ = f"{prefix}__"
        if x.startswith(prefix__):
            return x[len(prefix__) :]
        # The way this is used below, this else shouldn't really execute
        # But its here for completeness in case something goes wrong
        else:
            return x  # pragma: no cover

    # Handle passage of certain scalar values
    if isinstance(keys, (str, float, int, bool, type)):
        keys = [keys]

    if prefix is not None:
        keys = [f"{prefix}__{key}" for key in keys]
    else:
        keys = list(keys)
    subsetted_dict = {rem_prefix(k): v for k, v in input_dict.items() if k in keys}

    return subsetted_dict
