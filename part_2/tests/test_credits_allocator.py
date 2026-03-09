import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.credits_allocator import credits_allocator

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_preserves_length(total, weights):
    allocations = credits_allocator(total, weights)
    assert len(allocations) == len(weights)

@given(total=st.integers(max_value=-1), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_branch_specific_behavior_total_less_than_zero(total, weights):
    with pytest.raises(ValueError):
        credits_allocator(total, weights)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(max_value=-1))
def test_branch_specific_behavior_minimum_less_than_zero(total, weights, minimum):
    with pytest.raises(ValueError):
        credits_allocator(total, weights, minimum=minimum)

@given(total=st.integers(min_value=0))
def test_branch_specific_behavior_weights_empty(total):
    with pytest.raises(ValueError):
        credits_allocator(total, [])

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1))
def test_branch_specific_behavior_all_weights_zero(total, weights):
    with pytest.raises(ValueError):
        credits_allocator(total, weights)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_loop_invariant_each_allocation_ge_minimum(total, weights):
    minimum = 0
    allocations = credits_allocator(total, weights, minimum=minimum)
    assert all(a >= minimum for a in allocations)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_loop_invariant_sum_allocations_le_total(total, weights):
    allocations = credits_allocator(total, weights)
    assert sum(allocations) <= total

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_return_postcondition(total, weights):
    allocations = credits_allocator(total, weights)
    assert isinstance(allocations, list)
    assert all(isinstance(a, int) for a in allocations)
    assert len(allocations) == len(weights)