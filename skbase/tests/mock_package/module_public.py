# -*- coding: utf-8 -*-
"""Public module in mock package with decorated and plain functions."""

from functools import wraps


def simple_function(x):
    """A plain function for testing function discovery."""
    return x * 2


def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@my_decorator
def decorated_function(y):
    """A decorated function to ensure unwrapping works in member discovery."""
    return y + 1


__all__ = ["simple_function", "decorated_function"]
