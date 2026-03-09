import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.calibrate_loss import calibrate_loss

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats())
def test_raises_value_error_on_degenerate_segment(x0, y0, x1, y1):
    with pytest.raises(ValueError):
        calibrate_loss(x0, y0, x1, y1, x0)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_returns_correct_linear_interpolation(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
    result = calibrate_loss(x0, y0, x1, y1, x, clamp=False)
    assert result == pytest.approx(expected)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_applies_clamping_when_enabled(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    result = calibrate_loss(x0, y0, x1, y1, x, clamp=True)
    assert min(y0, y1) <= result <= max(y0, y1)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_skips_clamping_when_disabled(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    result = calibrate_loss(x0, y0, x1, y1, x, clamp=False)
    expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
    assert result == pytest.approx(expected)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_clamps_to_minimum_when_below_range(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    expected = min(y0, y1)
    result = calibrate_loss(x0, y0, x1, y1, x, clamp=True)
    if result < expected:
        assert result == expected

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_clamps_to_maximum_when_above_range(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    expected = max(y0, y1)
    result = calibrate_loss(x0, y0, x1, y1, x, clamp=True)
    if result > expected:
        assert result == expected

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_return_postcondition(x0, y0, x1, y1, x):
    if x1 == x0:
        pytest.skip("degenerate segment")
    result = calibrate_loss(x0, y0, x1, y1, x, clamp=True)
    assert isinstance(result, float)