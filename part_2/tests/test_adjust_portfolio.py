import hypothesis
from hypothesis import given, strategies as st
import pytest

# Assuming the function is in the same file for testing purposes
def adjust_portfolio(current, target, *, damping=0.5):
    """
    Rebalance portfolio allocations toward target mix.
    """
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = []
    for c, t in zip(current, target):
        adjusted.append(c + (t - c) * damping)

    # BUG: missing normalization; totals can drift.
    return adjusted

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            adjust_portfolio(current, target, damping=damping)
    else:
        result = adjust_portfolio(current, target, damping=damping)
        assert len(result) == len(current)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_branch_shape_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            adjust_portfolio(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=0), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_branch_empty_allocation(current, target, damping):
    if not current:
        with pytest.raises(ValueError, match="empty allocation"):
            adjust_portfolio(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_loop_invariant(current, target, damping):
    if len(current) == len(target) and current:
        result = adjust_portfolio(current, target, damping=damping)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_return_postcondition(current, target, damping):
    if len(current) == len(target) and current:
        result = adjust_portfolio(current, target, damping=damping)
        assert isinstance(result, list)
        assert len(result) == len(current)