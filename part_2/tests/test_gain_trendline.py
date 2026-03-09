import hypothesis
from hypothesis import given
import hypothesis.strategies as st
from dataset.python_programs.gain_trendline import gain_trendline

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_preserves_length(x0, y0, x1, y1, x):
    result = gain_trendline(x0, y0, x1, y1, x)
    assert len([result]) == 1

@given(x0=st.floats(), y0=st.floats(), x=st.floats())
def test_branch_specific_behavior_degenerate_segment(x0, y0, x):
    with hypothesis.raises(ValueError):
        gain_trendline(x0, y0, x0, y0, x)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_clamp(x0, y0, x1, y1, x):
    result = gain_trendline(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    assert lo <= result <= hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_y_less_than_lo(x0, y0, x1, y1, x):
    result = gain_trendline(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    if result < lo:
        assert result == lo

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_y_greater_than_hi(x0, y0, x1, y1, x):
    result = gain_trendline(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    if result > hi:
        assert result == hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_return_postcondition(x0, y0, x1, y1, x):
    result = gain_trendline(x0, y0, x1, y1, x)
    assert isinstance(result, (int, float))