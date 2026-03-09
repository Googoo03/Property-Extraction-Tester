import hypothesis
from hypothesis import given, strategies as st
import pytest

def test_raises_value_error_on_degenerate_segment():
    with pytest.raises(ValueError):
        coverage_interp(0, 0, 0, 1, 0)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_returns_correct_linear_interpolation(x0, y0, x1, y1, x):
    if x1 == x0:
        with pytest.raises(ValueError):
            coverage_interp(x0, y0, x1, y1, x)
    else:
        expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
        assert coverage_interp(x0, y0, x1, y1, x) == expected

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_clamps_output_to_y_range_when_enabled(x0, y0, x1, y1, x):
    if x1 != x0:
        expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        clamped = max(lo, min(hi, expected))
        assert coverage_interp(x0, y0, x1, y1, x, clamp=True) == clamped

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_returns_unclamped_value_when_disabled(x0, y0, x1, y1, x):
    if x1 != x0:
        expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
        assert coverage_interp(x0, y0, x1, y1, x, clamp=False) == expected

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_clamps_to_minimum_when_below_range(x0, y0, x1, y1, x):
    if x1 != x0:
        expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        if expected < lo:
            assert coverage_interp(x0, y0, x1, y1, x, clamp=True) == lo

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_clamps_to_maximum_when_above_range(x0, y0, x1, y1, x):
    if x1 != x0:
        expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        if expected > hi:
            assert coverage_interp(x0, y0, x1, y1, x, clamp=True) == hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_returns_value_satisfying_expected_semantics(x0, y0, x1, y1, x):
    if x1 == x0:
        with pytest.raises(ValueError):
            coverage_interp(x0, y0, x1, y1, x)
    else:
        expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        if coverage_interp(x0, y0, x1, y1, x, clamp=True) < lo:
            assert coverage_interp(x0, y0, x1, y1, x, clamp=True) == lo
        elif coverage_interp(x0, y0, x1, y1, x, clamp=True) > hi:
            assert coverage_interp(x0, y0, x1, y1, x, clamp=True) == hi
        else:
            assert coverage_interp(x0, y0, x1, y1, x, clamp=True) == expected