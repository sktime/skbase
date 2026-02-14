# -*- coding: utf-8 -*-
"""Public module in mock package with decorated and plain functions."""

from functools import wraps


def simple_function(x):
    """Double the given input and return the result."""
    return x * 2


def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@my_decorator
def decorated_function(y):
    """Increment the given input by one and return the result."""
    return y + 1


__all__ = ["simple_function", "decorated_function"]
