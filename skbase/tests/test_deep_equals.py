from skbase.utils.deep_equals import deep_equals


def test_deep_equals_numpy_string_array():
    """Test that deep_equals works on string-dtype numpy arrays. GitHub issue #517."""
    import numpy as np

    s = np.array(["1", "2", "1"])
    # Same arrays should be equal
    assert deep_equals(s, s) is True

    # Different arrays should not be equal
    t = np.array(["1", "2", "3"])
    assert deep_equals(s, t) is False


def test_deep_equals_equal_object():
    class DummyComposite:
        def __init__(self, func1, func2, neq_called):
            self.func1 = func1
            self.func2 = func2
            self.neq_called = neq_called

    class Dummy:
        def __init__(self, func):
            self.func = func

        def __eq__(self, other) -> DummyComposite:
            return DummyComposite(self.func, other.func, False)

        def __ne__(self, other) -> DummyComposite:
            return DummyComposite(self.func, other.func, True)

    a = Dummy(lambda x: x)
    assert deep_equals(a, a)
