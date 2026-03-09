import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.shift_demand import shift_demand

# Property: preserves_length
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            shift_demand(current, target, damping=damping)
    else:
        result = shift_demand(current, target, damping=damping)
        assert len(result) == len(current)

# Property: branch_specific_behavior (shape mismatch)
@given(current=st.lists(st.floats()), target=st.lists(st.floats()), damping=st.floats())
def test_shape_mismatch_raises_value_error(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            shift_demand(current, target, damping=damping)

# Property: branch_specific_behavior (empty allocation)
@given(damping=st.floats())
def test_empty_allocation_raises_value_error(damping):
    with pytest.raises(ValueError, match="empty allocation"):
        shift_demand([], [], damping=damping)

# Property: loop_invariant
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_loop_invariant(current, target, damping):
    if len(current) == len(target):
        result = shift_demand(current, target, damping=damping)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping

# Property: return_postcondition
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_return_postcondition(current, target, damping):
    if len(current) == len(target):
        result = shift_demand(current, target, damping=damping)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping