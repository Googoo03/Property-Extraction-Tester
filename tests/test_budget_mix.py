import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.budget_mix import budget_mix

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            budget_mix(current, target, damping=damping)
    else:
        result = budget_mix(current, target, damping=damping)
        assert len(result) == len(current)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_length_mismatch(current, target):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            budget_mix(current, target)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_branch_specific_behavior_empty_current(current, target, damping):
    if not current:
        with pytest.raises(ValueError):
            budget_mix(current, target, damping=damping)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_loop_invariant(current, target, damping):
    if len(current) == len(target) and current:
        result = budget_mix(current, target, damping=damping)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_return_postcondition(current, target, damping):
    if len(current) == len(target) and current:
        result = budget_mix(current, target, damping=damping)
        assert isinstance(result, list)
        assert len(result) == len(current)