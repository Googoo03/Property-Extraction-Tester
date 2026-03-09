import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.adjust_supply import adjust_supply

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_preserves_length(current, target, damping):
    if len(current) == len(target):
        result = adjust_supply(current, target, damping=damping)
        assert len(result) == len(current)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_branch_specific_behavior_length_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            adjust_supply(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=0), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_branch_specific_behavior_empty_current(current, target, damping):
    if not current:
        with pytest.raises(ValueError, match="empty allocation"):
            adjust_supply(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_loop_invariant(current, target, damping):
    if len(current) == len(target):
        result = adjust_supply(current, target, damping=damping)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_return_postcondition(current, target, damping):
    if len(current) == len(target):
        result = adjust_supply(current, target, damping=damping)
        expected = [current[i] + (target[i] - current[i]) * damping for i in range(len(current))]
        assert result == expected

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_non_empty_input(current, target, damping):
    if len(current) > 0 and len(current) == len(target):
        result = adjust_supply(current, target, damping=damping)
        assert result is not None

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_matching_shapes(current, target, damping):
    if len(current) == len(target):
        result = adjust_supply(current, target, damping=damping)
        assert len(result) == len(current)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_correct_update_formula(current, target, damping):
    if len(current) == len(target):
        result = adjust_supply(current, target, damping=damping)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_all_indices_processed(current, target, damping):
    if len(current) == len(target):
        result = adjust_supply(current, target, damping=damping)
        assert len(result) == len(current)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_raises_value_error_shape_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            adjust_supply(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=0), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_raises_value_error_empty_allocation(current, target, damping):
    if not current:
        with pytest.raises(ValueError, match="empty allocation"):
            adjust_supply(current, target, damping=damping)