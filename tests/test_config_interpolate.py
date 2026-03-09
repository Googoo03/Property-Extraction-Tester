import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.config_interpolate import config_interpolate

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_config_interpolate_preserves_length(x0, y0, x1, y1, x):
    result = config_interpolate(x0, y0, x1, y1, x)
    assert isinstance(result, (int, float))

@given(x0=st.floats(), y0=st.floats(), x=st.floats())
def test_config_interpolate_raises_value_error_when_x1_equals_x0(x0, y0, x):
    with pytest.raises(ValueError):
        config_interpolate(x0, y0, x0, y0, x)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_config_interpolate_behavior_depends_on_clamp(x0, y0, x1, y1, x):
    result_clamped = config_interpolate(x0, y0, x1, y1, x, clamp=True)
    result_unclamped = config_interpolate(x0, y0, x1, y1, x, clamp=False)
    assert result_clamped != result_unclamped

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_config_interpolate_y_set_to_lo_when_y_lt_lo_and_clamp_true(x0, y0, x1, y1, x):
    y = config_interpolate(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    if y < lo:
        assert y == lo

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_config_interpolate_y_set_to_hi_when_y_gt_hi_and_clamp_true(x0, y0, x1, y1, x):
    y = config_interpolate(x0, y0, x1, y1, x, clamp=True)
    lo, hi = min(y0, y1), max(y0, y1)
    if y > hi:
        assert y == hi

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats())
def test_config_interpolate_return_value_satisfies_expected_semantics(x0, y0, x1, y1, x):
    y = config_interpolate(x0, y0, x1, y1, x)
    t = (x - x0) / (x1 - x0)
    expected_y = y0 + t * (y1 - y0)
    assert y == expected_y