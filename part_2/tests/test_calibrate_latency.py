import pytest
from hypothesis import given, strategies as st
from math import isclose

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_calibrate_latency_preserves_length(x0, y0, x1, y1, x):
    result = calibrate_latency(x0, y0, x1, y1, x)
    assert isinstance(result, float)

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False)
)
def test_calibrate_latency_branch_specific_behavior_zero_length(x0, y0, x, y1):
    with pytest.raises(ValueError, match="zero length"):
        calibrate_latency(x0, y0, x0, y1, x)

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_calibrate_latency_branch_specific_behavior_clamp(x0, y0, x1, y1, x):
    result = calibrate_latency(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert low <= result <= high

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_calibrate_latency_return_postcondition(x0, y0, x1, y1, x):
    if x1 != x0:
        result = calibrate_latency(x0, y0, x1, y1, x)
        t = (x - x0) / (x1 - x0)
        expected = (1 - t) * y0 + t * y1
        if x1 > x0:
            assert isclose(result, expected) or (min(y0, y1) <= result <= max(y0, y1))
        else:
            assert isclose(result, expected) or (min(y0, y1) <= result <= max(y0, y1))