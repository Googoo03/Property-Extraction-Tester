import hypothesis
import hypothesis.strategies as st
from hypothesis import given, assume
from dataset.python_programs.model_confidence_clamp import model_confidence_clamp

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_preserve_length(x0, y0, x1, y1, x, clamp):
    output = model_confidence_clamp(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(output, float)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_branch_specific_behavior_x0_equals_x1(x0, y0, x1, y1, x, clamp):
    assume(x0 == x1)
    try:
        model_confidence_clamp(x0, y0, x1, y1, x, clamp=clamp)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError when x0 == x1"

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_branch_specific_behavior_clamp(x0, y0, x1, y1, x, clamp):
    y = model_confidence_clamp(x0, y0, x1, y1, x, clamp=clamp)
    low, high = min(y0, y1), max(y0, y1)
    if clamp:
        assert low <= y <= high
    else:
        assert True

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_return_postcondition(x0, y0, x1, y1, x, clamp):
    y = model_confidence_clamp(x0, y0, x1, y1, x, clamp=clamp)
    t = (x - x0) / (x1 - x0)
    expected_y = y0 + t * (y1 - y0)
    assert y == expected_y

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_x0_not_equal_x1(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    try:
        model_confidence_clamp(x0, y0, x1, y1, x, clamp=clamp)
    except ValueError:
        assert False, "Unexpected ValueError when x0 != x1"

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_clamp_boolean(x0, y0, x1, y1, x, clamp):
    assert isinstance(clamp, bool)

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_t_in_range(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    t = (x - x0) / (x1 - x0)
    assert 0 <= t <= 1

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_y_within_bounds(x0, y0, x1, y1, x, clamp):
    y = model_confidence_clamp(x0, y0, x1, y1, x, clamp=clamp)
    low, high = min(y0, y1), max(y0, y1)
    if clamp:
        assert low <= y <= high
    else:
        assert True

@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_linear_interpolation(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    t = (x - x0) / (x1 - x0)
    y = y0 + t * (y1 - y0)
    assert model_confidence_clamp(x0, y0, x1, y1, x, clamp=clamp) == y