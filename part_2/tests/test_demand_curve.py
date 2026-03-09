import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.demand_curve import demand_curve

# Property: preserves_length
@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_preserves_length(x0, y0, x1, y1, x):
    result = demand_curve(x0, y0, x1, y1, x)
    assert isinstance(result, (int, float))

# Property: branch_specific_behavior (x1 == x0)
@given(
    x0=st.floats(),
    y0=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_zero_length_branch(x0, y0, y1, x):
    with pytest.raises(ValueError, match="zero length"):
        demand_curve(x0, y0, x0, y1, x)

# Property: branch_specific_behavior (clamp)
@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_clamp_behavior(x0, y0, x1, y1, x):
    result = demand_curve(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert low <= result <= high

# Property: return_postcondition
@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_return_type(x0, y0, x1, y1, x):
    result = demand_curve(x0, y0, x1, y1, x)
    assert isinstance(result, (int, float))