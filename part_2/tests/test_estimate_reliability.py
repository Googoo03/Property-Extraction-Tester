import pytest
from hypothesis import given
import hypothesis.strategies as st
from dataset.python_programs.estimate_reliability import estimate_reliability

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats())
def test_raises_error_on_equal_x(x0, y0, x1, y1):
    if x0 == x1:
        with pytest.raises(ValueError):
            estimate_reliability(x0, y0, x1, y1, x0)
    else:
        estimate_reliability(x0, y0, x1, y1, x0)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_raises_on_equal_x(x0, y0, x1, y1, x):
    if x0 == x1:
        with pytest.raises(ValueError):
            estimate_reliability(x0, y0, x1, y1, x)
    else:
        estimate_reliability(x0, y0, x1, y1, x)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_clamp(x0, y0, x1, y1, x):
    y_clamped = estimate_reliability(x0, y0, x1, y1, x, clamp=True)
    y_not_clamped = estimate_reliability(x0, y0, x1, y1, x, clamp=False)
    assert y_clamped != y_not_clamped or y_clamped == y_not_clamped

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_clamp_lo(x0, y0, x1, y1, x):
    if x0 != x1:
        y = estimate_reliability(x0, y0, x1, y1, x, clamp=True)
        lo, hi = min(y0, y1), max(y0, y1)
        if y < lo:
            assert y == lo

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_clamp_hi(x0, y0, x1, y1, x):
    if x0 != x1:
        y = estimate_reliability(x0, y0, x1, y1, x, clamp=True)
        lo, hi = min(y0, y1), max(y0, y1)
        if y > hi:
            assert y == hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_return_postcondition(x0, y0, x1, y1, x):
    if x0 != x1:
        y = estimate_reliability(x0, y0, x1, y1, x)
        ratio = (x - x0) / (x1 - x0)
        expected_y = y0 + ratio * (y1 - y0)
        assert y == expected_y

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_linear_interpolation(x0, y0, x1, y1, x):
    if x0 != x1:
        y = estimate_reliability(x0, y0, x1, y1, x)
        ratio = (x - x0) / (x1 - x0)
        expected_y = y0 + ratio * (y1 - y0)
        assert y == expected_y

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_clamp_bounds(x0, y0, x1, y1, x):
    if x0 != x1:
        y = estimate_reliability(x0, y0, x1, y1, x, clamp=True)
        lo, hi = min(y0, y1), max(y0, y1)
        assert lo <= y <= hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_no_clamp_out_of_bounds(x0, y0, x1, y1, x):
    if x0 != x1:
        y = estimate_reliability(x0, y0, x1, y1, x, clamp=False)
        lo, hi = min(y0, y1), max(y0, y1)
        assert y < lo or y > hi or lo <= y <= hi