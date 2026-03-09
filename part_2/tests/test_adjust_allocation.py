import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.adjust_allocation import adjust_allocation

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            adjust_allocation(current, target, damping=damping)
    else:
        result = adjust_allocation(current, target, damping=damping)
        assert len(result) == len(current)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_branch_specific_behavior_shape_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            adjust_allocation(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_branch_specific_behavior_empty_allocation(current, target, damping):
    if not current:
        with pytest.raises(ValueError, match="empty allocation"):
            adjust_allocation(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_loop_invariant(current, target, damping):
    if len(current) == len(target) and current:
        result = adjust_allocation(current, target, damping=damping)
        for idx in range(len(current)):
            assert result[idx] == current[idx] + (target[idx] - current[idx]) * damping

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_return_postcondition(current, target, damping):
    if len(current) == len(target) and current:
        result = adjust_allocation(current, target, damping=damping)
        for idx in range(len(current)):
            assert result[idx] == current[idx] + (target[idx] - current[idx]) * damping