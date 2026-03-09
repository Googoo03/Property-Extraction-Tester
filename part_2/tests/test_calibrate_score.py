import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.calibrate_score import calibrate_score

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_linear_interpolation(x0, y0, x1, y1, x):
    if x1 == x0:
        with pytest.raises(ValueError):
            calibrate_score(x0, y0, x1, y1, x)
    else:
        result = calibrate_score(x0, y0, x1, y1, x, clamp=False)
        t = (x - x0) / (x1 - x0)
        expected = y0 + t * (y1 - y0)
        assert result == expected

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_raises_error_on_degenerate_segment(x0, y0, x1, y1, x):
    if x1 == x0:
        with pytest.raises(ValueError):
            calibrate_score(x0, y0, x1, y1, x)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_no_clamping(x0, y0, x1, y1, x):
    if x1 != x0:
        result = calibrate_score(x0, y0, x1, y1, x, clamp=False)
        t = (x - x0) / (x1 - x0)
        expected = y0 + t * (y1 - y0)
        assert result == expected

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_clamps_output_to_y_range(x0, y0, x1, y1, x):
    if x1 != x0:
        result = calibrate_score(x0, y0, x1, y1, x, clamp=True)
        lo, hi = min(y0, y1), max(y0, y1)
        assert lo <= result <= hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_extrapolation_below(x0, y0, x1, y1, x):
    if x1 != x0 and x < x0:
        result = calibrate_score(x0, y0, x1, y1, x, clamp=False)
        assert result < y0

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_extrapolation_above(x0, y0, x1, y1, x):
    if x1 != x0 and x > x1:
        result = calibrate_score(x0, y0, x1, y1, x, clamp=False)
        assert result > y1