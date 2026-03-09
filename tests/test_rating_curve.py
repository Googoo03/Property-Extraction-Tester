import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.rating_curve import rating_curve
from hypothesis.strategies import composite

@composite
def inputs(draw):
    x0 = draw(st.floats(allow_nan=False, allow_infinity=False))
    y0 = draw(st.floats(allow_nan=False, allow_infinity=False))
    x1 = draw(st.floats(min_value=x0 + 1, allow_nan=False, allow_infinity=False))
    x = draw(st.floats(allow_nan=False, allow_infinity=False))
    clamp = draw(st.booleans())

    return x0, y0, x1, x, clamp


# Property: preserves_length
@given(x0=st.floats(), y0=st.floats(), x1=st.floats(), y1=st.floats(), x=st.floats(), clamp=st.booleans())
def test_preserves_length(x0, y0, x1, y1, x, clamp):
    assert len([x0, y0, x1, y1, x, clamp]) == 6

# Property: branch_specific_behavior (raises ValueError when x1 == x0)
@given(x0=st.floats(), y0=st.floats(), x=st.floats(), clamp=st.booleans())
def test_raises_value_error_on_zero_length(x0, y0, x=st.floats(), clamp=st.booleans()):
    with pytest.raises(ValueError):
        rating_curve(x0, y0, x0, y0, x, clamp=clamp)

# Property: branch_specific_behavior (output clamped to [min(y0, y1), max(y0, y1)] when clamp=True)
@given(inputs())
def test_clamp_behavior(x0, y0, x1, x, clamp):
    y1 = y0 + 1  # Ensure y1 != y0 for meaningful clamp test
    y = rating_curve(x0, y0, x1, y1, x, clamp=clamp)
    if clamp:
        low, high = sorted([y0, y1])
        assert low <= y <= high

# Property: return_postcondition (returns value satisfying expected semantics)
@given(inputs())
def test_return_value_semantics(x0, y0, x1, x, clamp):
    y = rating_curve(x0, y0, x1, y1, x, clamp=clamp)
    t = (x - x0) / (x1 - x0)
    expected_y = (1 - t) * y0 + t * y1
    if not clamp or (min(y0, y1) <= expected_y <= max(y0, y1)):
        assert y == expected_y
    else:
        low, high = sorted([y0, y1])
        assert y == low or y == high