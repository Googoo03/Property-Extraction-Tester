import hypothesis
from hypothesis import given
import hypothesis.strategies as st
import pytest
from dataset.python_programs.shift_risk import shift_risk

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1))
def test_preserves_length(current, target):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            shift_risk(current, target)
    else:
        result = shift_risk(current, target)
        assert len(result) == len(current)

@given(current=st.lists(st.floats()), target=st.lists(st.floats()))
def test_branch_specific_behavior_shape_mismatch(current, target):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            shift_risk(current, target)

@given(current=st.lists(st.floats()), target=st.lists(st.floats()))
def test_branch_specific_behavior_empty_allocation(current, target):
    if not current:
        with pytest.raises(ValueError, match="empty allocation"):
            shift_risk(current, target)

@given(current=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1), target=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1), damping=st.floats(min_value=0, max_value=1))
def test_loop_invariant(current, target, damping):
    if len(current) == len(target):
        result = shift_risk(current, target, damping=damping)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping

@given(current=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1), target=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1), damping=st.floats(min_value=0, max_value=1))
def test_return_postcondition(current, target, damping):
    if len(current) == len(target):
        result = shift_risk(current, target, damping=damping)
        assert isinstance(result, list)
        assert all(isinstance(x, float) for x in result)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping