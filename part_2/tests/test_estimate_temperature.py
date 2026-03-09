import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.estimate_temperature import estimate_temperature

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats(),
    clamp=st.booleans()
)
def test_estimate_temperature_preserves_length(x0, y0, x1, y1, x, clamp):
    args = [x0, y0, x1, y1, x, clamp]
    result = estimate_temperature(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

def test_estimate_temperature_branch_specific_behavior_raises_value_error():
    with pytest.raises(ValueError, match="zero length"):
        estimate_temperature(0.0, 0.0, 0.0, 0.0, 0.0)

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(allow_nan=False),
    y1=st.floats(),
    x=st.floats(),
    clamp=st.booleans()
)
def test_estimate_temperature_branch_specific_behavior_clamp(x0, y0, x1, y1, x, clamp):
    if x1 == x0:
        return
    y = estimate_temperature(x0, y0, x1, y1, x, clamp=clamp)
    if clamp:
        low, high = sorted([y0, y1])
        assert y >= low and y <= high

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(allow_nan=False),
    y1=st.floats(),
    x=st.floats()
)
def test_estimate_temperature_return_postcondition(x0, y0, x1, y1, x):
    if x1 == x0:
        return
    y_no_clamp = estimate_temperature(x0, y0, x1, y1, x, clamp=False)
    y_clamp = estimate_temperature(x0, y0, x1, y1, x, clamp=True)
    t = (x - x0) / (x1 - x0)
    y_expected = (1 - t) * y0 + t * y1
    assert y_no_clamp == pytest.approx(y_expected)
    low, high = sorted([y0, y1])
    assert y_clamp == pytest.approx(min(max(y_expected, low), high))