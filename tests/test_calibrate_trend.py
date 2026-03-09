import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.calibrate_trend import calibrate_trend

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_calibrate_trend_preserves_length(x0, y0, x1, y1, x):
    output = calibrate_trend(x0, y0, x1, y1, x)
    assert len([output]) == 1

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False)
)
def test_calibrate_trend_branch_specific_behavior_zero_length(x0, y0, x, y1):
    with pytest.raises(ValueError, match="zero length"):
        calibrate_trend(x0, y0, x0, y1, x)

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_calibrate_trend_branch_specific_behavior_clamp(x0, y0, x1, y1, x):
    y = calibrate_trend(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert low <= y <= high

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_calibrate_trend_return_postcondition(x0, y0, x1, y1, x):
    y = calibrate_trend(x0, y0, x1, y1, x)
    assert isinstance(y, float)