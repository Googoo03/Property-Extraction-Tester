import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.bandwidth_rebalance import bandwidth_rebalance

# Property: preserves_length
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1))
def test_preserves_length(current, target):
    if len(current) == len(target):
        result = bandwidth_rebalance(current, target)
        assert len(result) == len(current)

# Property: branch_specific_behavior (len(current) != len(target))
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=2))
def test_branch_length_mismatch_raises_value_error(current, target):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            bandwidth_rebalance(current, target, target)

# Property: branch_specific_behavior (not current)
@given(current=st.lists(st.floats(), min_size=0), target=st.lists(st.floats(), min_size=1))
def test_branch_empty_current_raises_value_error(current, target):
    if not current:
        with pytest.raises(ValueError, match="empty allocation"):
            bandwidth_rebalance(current, target)

# Property: loop_invariant
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1))
def test_loop_invariant(current, target):
    if len(current) == len(target) and current:
        damping = 0.7
        result = bandwidth_rebalance(current, target)
        for idx in range(len(current)):
            expected = current[idx] + (target[idx] - current[idx]) * damping
            assert abs(result[idx] - expected) < 1e-9

# Property: return_postcondition
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1))
def test_return_postcondition(current, target):
    if len(current) == len(target) and current:
        damping = 0.7
        result = bandwidth_rebalance(current, target)
        for idx in range(len(current)):
            assert result[idx] == current[idx] + (target[idx] - current[idx]) * damping