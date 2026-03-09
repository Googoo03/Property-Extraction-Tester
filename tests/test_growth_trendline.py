import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.growth_trendline import growth_trendline

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats())
def test_raises_error_on_degenerate_segment(x0, y0, x1, y1):
    with pytest.raises(ValueError):
        growth_trendline(x0, y0, x1, y1, x0)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_correct_interpolation(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
    assert growth_trendline(x0, y0, x1, y1, x, clamp=True) == expected

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_clamp_uses_y_range(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    y = growth_trendline(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    assert lo <= y <= hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_no_clamp_by_default(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    unclamped = growth_trendline(x0, y0, x1, y1, x, clamp=False)
    clamped = growth_trendline(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    if not (lo <= unclamped <= hi):
        assert unclamped == clamped

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_return_postcondition(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    y = growth_trendline(x0, y0, x1, y1, x)
    expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
    assert y == expected