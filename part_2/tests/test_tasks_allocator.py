import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.tasks_allocator import tasks_allocator

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1))
def test_preserves_length(total, weights):
    result = tasks_allocator(total, weights)
    assert len(result) == len(weights)

@given(total=st.integers(max_value=-1), weights=st.lists(st.integers(min_value=0), min_size=1))
def test_branch_total_negative(total, weights):
    with pytest.raises(ValueError, match="total must be non-negative"):
        tasks_allocator(total, weights)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1), minimum=st.integers(max_value=-1))
def test_branch_minimum_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="minimum must be non-negative"):
        tasks_allocator(total, weights, minimum=minimum)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=0))
def test_branch_no_weights(total, weights):
    if not weights:
        with pytest.raises(ValueError, match="no weights provided"):
            tasks_allocator(total, weights)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1))
def test_branch_all_weights_zero(total, weights):
    if all(w == 0 for w in weights):
        with pytest.raises(ValueError, match="all weights are zero"):
            tasks_allocator(total, weights)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1))
def test_loop_invariant_minimum_and_total(total, weights):
    result = tasks_allocator(total, weights)
    assert all(minimum <= x <= total for x in result)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1))
def test_loop_invariant_sum_allocation(total, weights):
    result = tasks_allocator(total, weights)
    assert sum(result) <= total

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1))
def test_return_postcondition(total, weights):
    result = tasks_allocator(total, weights)
    assert isinstance(result, list)
    assert all(isinstance(x, int) for x in result)
    assert all(minimum <= x <= total for x in result)
    assert len(result) == len(weights)