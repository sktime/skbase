# -*- coding: utf-8 -*-
"""Utilities for handling the random_state variable."""

__author__ = ["fkiraly"]


def set_random_state(estimator, random_state=None, deep=True, root_policy="copy"):
    """Set random_state pseudo-random seed parameters for an estimator.

    Finds ``random_state`` named parameters via ``estimator.get_params``,
    and sets them to integers derived from ``random_state`` via ``set_params``.
    These integers are sampled from chain hashing via ``sample_dependent_seed``,
    and guarantee pseudo-random independence of seeded random generators.

    Applies to ``random_state`` parameters in ``estimator`` depending on
    ``root_policy``, and remaining component estimators if and only if ``deep=True``.

    Note: calls ``estimator.set_params`` even if ``estimator``
    does not have a ``random_state``,
    or none of its components have a ``random_state`` parameter.
    Therefore, ``set_random_state`` will reset any ``scikit-base`` estimator,
    even those without a ``random_state`` parameter.

    Parameters
    ----------
    estimator : estimator supporting get_params, set_params
        Estimator with potential randomness managed by random_state parameters.

    random_state : int, RandomState instance or None, default=None
        Pseudo-random number generator to control the generation of the random
        integers. Pass an int for reproducible output across multiple function calls.

    deep : bool, default=True
        Whether to set the random state in sub-estimators.
        If False, will set only ``estimator``'s ``random_state`` parameter, if exists.
        If True, will set ``random_state`` parameters in sub-estimators as well.

    root_policy : str, one of {"copy", "keep", "new"}, default="copy"

        * "copy" : ``estimator.random_state`` is set to input ``random_state``
        * "keep" : ``estimator.random_state`` is kept as is
        * "new" : ``estimator.random_state`` is set to a new random state,
          derived from input ``random_state``, and in general different from it

    Returns
    -------
    estimator : estimator
        reference to ``estimator`` with state changed, random seed set
    """
    random_state_orig = random_state
    random_state = check_random_state(random_state)

    keys = []
    for key in sorted(estimator.get_params(deep=True)):
        if key == "random_state" and root_policy != "keep":
            keys.append(key)
        if key.endswith("__random_state") and deep:
            keys.append(key)

    seeds = sample_dependent_seed(random_state, n_seeds=len(keys))
    to_set = dict(zip(keys, seeds))

    if root_policy == "copy" and "random_state" in to_set:
        to_set["random_state"] = random_state_orig

    estimator.set_params(**to_set)
    return estimator


# This function is copied from scikit-learn (sklearn.utils)
def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance.

    Parameters
    ----------
    seed : None, int or instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.
    """
    import numbers

    import numpy as np

    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, numbers.Integral):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError(
        "%r cannot be used to seed a numpy.random.RandomState instance" % seed
    )


def sample_dependent_seed(seed, n_seeds=None):
    """Sample one or multiple dependent seeds from a given seed.

    The sampled seeds are intended to be independent, pseudo-random uniform
    from the set of 256-bit integers.

    This is achieved by repeatedly hashing the seed using a cryptographic hash function,
    ``hashlib.sha256`` for SHA-256, and converting the hash to an integer.

    Parameters
    ----------
    seed : int (256-bit or less), bytes, or str coercible
        The seed to sample from.
    n_seeds : int, default=None
        The number of seeds to sample. If None, a single seed is sampled and returned.
        If an integer, a list of seeds of length ``n_seeds`` is sampled and returned.

    Returns
    -------
    int or list of ints, all 256-bit
        int if ``n_seeds`` is None, otherwise list of ints.
        The sampled seed(s).
    """
    if n_seeds is not None:
        seeds = []
        for _ in range(n_seeds):
            new_seed = sample_dependent_seed(seed)
            seeds.append(new_seed)
            seed = new_seed
        return seeds

    import hashlib

    # Convert the base seed to bytes
    seed_bytes = str(seed).encode("utf-8")

    # Use a cryptographic hash function (SHA-256) to generate a secure hash
    hash_object = hashlib.sha256(seed_bytes)
    hashed_seed = hash_object.hexdigest()

    # Convert the hashed seed to an integer
    new_seed = int(hashed_seed, 16)

    return new_seed
