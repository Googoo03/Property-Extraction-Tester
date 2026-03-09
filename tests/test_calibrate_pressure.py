import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.calibrate_pressure import calibrate_pressure

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_preserves_length(x0, y0, x1, y1, x):
    # The function returns a single float value, so length is always 1
    result = calibrate_pressure(x0, y0, x1, y1, x)
    assert isinstance(result, float)

@given(x0=st.floats(), y0=st.floats(), x=st.floats())
def test_branch_specific_behavior_zero_length_raises(x0, y0, x):
    with pytest.raises(ValueError, match="zero length"):
        calibrate_pressure(x0, y0, x0, y0, x)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_clamp_true(x0, y0, x1, y1, x):
    result = calibrate_pressure(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert low <= result <= high

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_branch_specific_behavior_clamp_false(x0, y0, x1, y1, x):
    result = calibrate_pressure(x0, y0, x1, y1, x, clamp=False)
    t = (x - x0) / (x1 - x0)
    expected = (1 - t) * y0 + t * y1
    assert result == expected

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_return_postcondition(x0, y0, x1, y1, x):
    result = calibrate_pressure(x0, y0, x1, y1, x)
    assert isinstance(result, float)