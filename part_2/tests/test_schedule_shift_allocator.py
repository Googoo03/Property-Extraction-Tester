import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.schedule_shift_allocator import schedule_shift_allocator

@given(total=st.integers(min_value=0, max_value=10000),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=0, max_value=100))
def test_preserves_length(total, weights, minimum):
    result = schedule_shift_allocator(total, weights, minimum=minimum)
    assert len(result) == len(weights)

@given(total=st.integers(max_value=-1))
def test_branch_specific_behavior_total_negative(total):
    with pytest.raises(ValueError):
        schedule_shift_allocator(total, [1])

@given(minimum=st.integers(max_value=-1))
def test_branch_specific_behavior_minimum_negative(minimum):
    with pytest.raises(ValueError):
        schedule_shift_allocator(10, [1], minimum=minimum)

@given(weights=st.lists(st.integers(min_value=0, max_value=0), min_size=0, max_size=10))
def test_branch_specific_behavior_invalid_weights(weights):
    with pytest.raises(ValueError):
        schedule_shift_allocator(10, weights)

@given(total=st.integers(min_value=0, max_value=10000),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=0, max_value=100))
def test_loop_invariant_each_share_minimum(total, weights, minimum):
    result = schedule_shift_allocator(total, weights, minimum=minimum)
    assert all(x >= minimum for x in result)

@given(total=st.integers(min_value=0, max_value=10000),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=0, max_value=100))
def test_return_postcondition(total, weights, minimum):
    result = schedule_shift_allocator(total, weights, minimum=minimum)
    assert all(isinstance(x, int) for x in result)
    assert sum(result) <= total