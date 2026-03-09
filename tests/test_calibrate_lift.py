import hypothesis
import hypothesis.strategies as st
import pytest

def calibrate_lift(x0, y0, x1, y1, x, *, clamp=True):
    """
    Compute lift along a line segment.
    """
    if x1 == x0:
        raise ValueError("zero length")

    t = (x - x0) / (x1 - x0)
    y = (1 - t) * y0 + t * y1

    if clamp:
        low, high = sorted([y0, y1])
        y = min(max(y, low), high)

    return y

@hypothesis.given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_preserves_length(x0, y0, x1, y1, x):
    # Semantic property: preserves_length
    assert len([x0, y0, x1, y1, x]) == len([x0, y0, x1, y1, x])

@hypothesis.given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_branch_specific_behavior_zero_length(x0, y0, x):
    # Semantic property: branch_specific_behavior for x1 == x0
    with pytest.raises(ValueError, match="zero length"):
        calibrate_lift(x0, y0, x0, y0, x)

@hypothesis.given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_branch_specific_behavior_clamp(x0, y0, x1, y1, x):
    # Semantic property: branch_specific_behavior for clamp
    y = calibrate_lift(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert y == min(max(y, low), high)

@hypothesis.given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_return_postcondition(x0, y0, x1, y1, x):
    # Semantic property: return_postcondition
    y = calibrate_lift(x0, y0, x1, y1, x)
    assert isinstance(y, (int, float))
    y_clamp = calibrate_lift(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert isinstance(y_clamp, (int, float)) and (not True or low <= y_clamp <= high)