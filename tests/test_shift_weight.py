import pytest
from hypothesis import given
from hypothesis import strategies as st
from dataset.python_programs.shift_weight import shift_weight

# Test for preserves_length property
@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_preserves_length(current, target, damping):
    if len(current) == len(target):
        result = shift_weight(current, target, damping=damping)
        assert len(result) == len(current)

# Test for branch_specific_behavior when len(current) != len(target)
@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=2),
       damping=st.floats(min_value=0, max_value=1))
def test_branch_length_mismatch_raises_value_error(current, target, damping):
    with pytest.raises(ValueError):
        shift_weight(current, target, damping=damping)

# Test for branch_specific_behavior when not current
@given(target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_branch_empty_current_raises_value_error(target, damping):
    with pytest.raises(ValueError):
        shift_weight([], target, damping=damping)

# Test for loop_invariant property
@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_loop_invariant(current, target, damping):
    if len(current) == len(target):
        result = shift_weight(current, target, damping=damping)
        for idx in range(len(current)):
            assert result[idx] == current[idx] + (target[idx] - current[idx]) * damping

# Test for return_postcondition property
@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_return_postcondition(current, target, damping):
    if len(current) == len(target):
        result = shift_weight(current, target, damping=damping)
        assert isinstance(result, list)
        assert all(isinstance(x, (int, float)) for x in result)