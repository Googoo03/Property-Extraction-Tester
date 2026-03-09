import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.estimate_supply import estimate_supply

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_estimate_supply_preserves_length(x0, y0, x1, y1, x):
    result = estimate_supply(x0, y0, x1, y1, x)
    assert isinstance(result, float)

@given(x0=st.floats(), y0=st.floats(), x=st.floats())
def test_estimate_supply_degenerate_segment_raises_value_error(x0, y0, x):
    with pytest.raises(ValueError, match='degenerate segment'):
        estimate_supply(x0, y0, x0, y0, x)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_estimate_supply_clamp_behavior(x0, y0, x1, y1, x):
    result_with_clamp = estimate_supply(x0, y0, x1, y1, x, clamp=True)
    result_without_clamp = estimate_supply(x0, y0, x1, y1, x, clamp=False)
    assert result_with_clamp == result_without_clamp

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_estimate_supply_clamp_lo_behavior(x0, y0, x1, y1, x):
    result = estimate_supply(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    if result < lo:
        assert result == lo

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_estimate_supply_clamp_hi_behavior(x0, y0, x1, y1, x):
    result = estimate_supply(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    if result > hi:
        assert result == hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_estimate_supply_return_postcondition(x0, y0, x1, y1, x):
    result = estimate_supply(x0, y0, x1, y1, x)
    assert isinstance(result, float)