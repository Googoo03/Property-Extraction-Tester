import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.probability_curve import probability_curve

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats(),
    clamp=st.booleans()
)
def test_preserves_length(x0, y0, x1, y1, x, clamp):
    args = [x0, y0, x1, y1, x, clamp]
    result = probability_curve(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(min_value=0.0, max_value=0.0),
    y1=st.floats(),
    x=st.floats(),
    clamp=st.booleans()
)
def test_branch_specific_behavior_degenerate_segment(x0, y0, x1, y1, x, clamp):
    with pytest.raises(ValueError, match="degenerate segment"):
        probability_curve(x0, y0, x1, y1, x, clamp=clamp)

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats(),
    clamp=st.booleans()
)
def test_branch_specific_behavior_clamp(x0, y0, x1, y1, x, clamp):
    result = probability_curve(x0, y0, x1, y1, x, clamp=clamp)
    if clamp:
        lo, hi = min(y0, y1), max(y0, y1)
        assert lo <= result <= hi
    else:
        t = (x - x0) / (x1 - x0)
        expected = y0 + t * (y1 - y0)
        assert result == expected

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats(),
    clamp=st.booleans()
)
def test_branch_specific_behavior_y_less_than_lo(x0, y0, x1, y1, x, clamp):
    if clamp:
        lo, hi = min(y0, y1), max(y0, y1)
        if y0 < y1:
            y = y0 - 1.0
        else:
            y = y1 - 1.0
        if y < lo:
            result = probability_curve(x0, y0, x1, y1, x, clamp=clamp)
            assert result >= lo

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats(),
    clamp=st.booleans()
)
def test_branch_specific_behavior_y_greater_than_hi(x0, y0, x1, y1, x, clamp):
    if clamp:
        lo, hi = min(y0, y1), max(y0, y1)
        if y0 < y1:
            y = y1 + 1.0
        else:
            y = y0 + 1.0
        if y > hi:
            result = probability_curve(x0, y0, x1, y1, x, clamp=clamp)
            assert result <= hi

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats(),
    clamp=st.booleans()
)
def test_return_postcondition(x0, y0, x1, y1, x, clamp):
    result = probability_curve(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)
    if not clamp or (min(y0, y1) <= result <= max(y0, y1)):
        t = (x - x0) / (x1 - x0)
        expected = y0 + t * (y1 - y0)
        assert result == expected