def test_deep_equals_numpy_string_array():
    """Test that deep_equals works on string-dtype numpy arrays. GitHub issue #517."""
    import numpy as np

    from skbase.utils.deep_equals import deep_equals

    s = np.array(["1", "2", "1"])
    # Same arrays should be equal
    assert deep_equals(s, s) is True

    # Different arrays should not be equal
    t = np.array(["1", "2", "3"])
    assert deep_equals(s, t) is False
