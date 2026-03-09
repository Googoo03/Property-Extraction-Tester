import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.speed_trendline import speed_trendline

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_x0_equals_x1(x0, y0, x1, y1, x):
    if x0 == x1:
        with pytest.raises(ValueError):
            speed_trendline(x0, y0, x1, y1, x)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_clamp_true(x0, y0, x1, y1, x):
    if x0 != x1:
        y = speed_trendline(x0, y0, x1, y1, x, clamp=True)
        lo, hi = min(y0, y1), max(y0, y1)
        assert lo <= y <= hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_y_less_than_lo(x0, y0, x1, y1, x):
    if x0 != x1:
        y = speed_trendline(x0, y0, x1, y1, x, clamp=True)
        lo, hi = min(y0, y1), max(y0, y1)
        if y < lo:
            assert y == lo

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_y_greater_than_hi(x0, y0, x1, y1, x):
    if x0 != x1:
        y = speed_trendline(x0, y0, x1, y1, x, clamp=True)
        lo, hi = min(y0, y1), max(y0, y1)
        if y > hi:
            assert y == hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_return_postcondition(x0, y0, x1, y1, x):
    if x0 != x1:
        y = speed_trendline(x0, y0, x1, y1, x)
        ratio = (x - x0) / (x1 - x0)
        expected_y = y0 + ratio * (y1 - y0)
        assert y == expected_y