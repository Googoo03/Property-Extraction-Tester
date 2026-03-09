import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.priority_mix import priority_mix

# Test for 'preserves_length' property
@given(
    current=st.lists(st.floats(), min_size=1),
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_preserves_length(current, target, damping):
    if len(current) == len(target):
        result = priority_mix(current, target, damping=damping)
        assert len(result) == len(current)

# Test for 'branch_specific_behavior' when len(current) != len(target)
@given(
    current=st.lists(st.floats(), min_size=1),
    target=st.lists(st.floats(), min_size=2),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_shape_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            priority_mix(current, target, damping=damping)

# Test for 'branch_specific_behavior' when not current
@given(
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_empty_allocation(target, damping):
    with pytest.raises(ValueError, match="empty allocation"):
        priority_mix([], target, damping=damping)

# Test for 'loop_invariant' property
@given(
    current=st.lists(st.floats(), min_size=1),
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_loop_invariant(current, target, damping):
    if len(current) == len(target):
        result = priority_mix(current, target, damping=damping)
        for idx in range(len(current)):
            assert result[idx] == current[idx] + (target[idx] - current[idx]) * damping

# Test for 'return_postcondition' property
@given(
    current=st.lists(st.floats(), min_size=1),
    target=st.lists(st.floats(), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_return_postcondition(current, target, damping):
    if len(current) == len(target):
        result = priority_mix(current, target, damping=damping)
        assert isinstance(result, list)
        assert len(result) == len(current)
        assert all(isinstance(x, (float, int)) for x in result)