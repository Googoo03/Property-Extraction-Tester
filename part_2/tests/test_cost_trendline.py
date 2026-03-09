import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.cost_trendline import cost_trendline

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_cost_trendline(x0, y0, x1, y1, x, clamp):
    if x0 == x1:
        with pytest.raises(ValueError):
            cost_trendline(x0, y0, x1, y1, x, clamp=clamp)
    else:
        result = cost_trendline(x0, y0, x1, y1, x, clamp=clamp)
        ratio = (x - x0) / (x1 - x0)
        y = y0 + ratio * (y1 - y0)
        if clamp:
            lo, hi = min(y0, y1), max(y0, y1)
            assert result == pytest.approx(min(max(y, lo), hi))
        else:
            assert result == pytest.approx(y)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_cost_trendline_no_clamping(x0, y0, x1, y1, x):
    if x0 != x1:
        result = cost_trendline(x0, y0, x1, y1, x, clamp=False)
        ratio = (x - x0) / (x1 - x0)
        y = y0 + ratio * (y1 - y0)
        assert result == pytest.approx(y)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_cost_trendline_clamping(x0, y0, x1, y1, x):
    if x0 != x1:
        result = cost_trendline(x0, y0, x1, y1, x, clamp=True)
        ratio = (x - x0) / (x1 - x0)
        y = y0 + ratio * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        assert result == pytest.approx(min(max(y, lo), hi))

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_cost_trendline_clamp_below(x0, y0, x1, y1, x):
    if x0 != x1:
        ratio = (x - x0) / (x1 - x0)
        y = y0 + ratio * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        if y < lo:
            result = cost_trendline(x0, y0, x1, y1, x, clamp=True)
            assert result == pytest.approx(lo)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_cost_trendline_clamp_above(x0, y0, x1, y1, x):
    if x0 != x1:
        ratio = (x - x0) / (x1 - x0)
        y = y0 + ratio * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        if y > hi:
            result = cost_trendline(x0, y0, x1, y1, x, clamp=True)
            assert result == pytest.approx(hi)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_cost_trendline_linear_interpolation(x0, y0, x1, y1, x):
    if x0 != x1:
        result = cost_trendline(x0, y0, x1, y1, x, clamp=False)
        ratio = (x - x0) / (x1 - x0)
        y = y0 + ratio * (y1 - y0)
        assert result == pytest.approx(y)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_cost_trendline_valid_input_range(x0, y0, x1, y1, x):
    if x0 == x1:
        with pytest.raises(ValueError):
            cost_trendline(x0, y0, x1, y1, x, clamp=True)
    else:
        result = cost_trendline(x0, y0, x1, y1, x, clamp=True)
        assert isinstance(result, float)