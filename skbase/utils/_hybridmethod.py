"""Decorator for methods that can be called both on the class and on instances."""


class hybridmethod:
    """Decorator for methods that can be called both on the class and on instances.

    The decorated method will receive the class as the first argument when called
    on the class, and the instance when called on an instance.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        """Get method that can be called on both class and instance."""
        def wrapper(*args, **kwargs):
            return self.func(obj if obj is not None else cls, *args, **kwargs)
        return wrapper
