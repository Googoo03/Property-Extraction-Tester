import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.quota_for_storage import quota_for_storage

# Test for preserving length
@given(total=st.integers(min_value=0, max_value=10000),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=0, max_value=100))
def test_preserve_length(total, weights, minimum):
    result = quota_for_storage(total, weights, minimum=minimum)
    assert len(result) == len(weights)

# Test for branch: total < 0
@given(total=st.integers(min_value=-10000, max_value=-1),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=0, max_value=100))
def test_branch_total_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="total must be non-negative"):
        quota_for_storage(total, weights, minimum=minimum)

# Test for branch: minimum < 0
@given(total=st.integers(min_value=0, max_value=10000),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=-100, max_value=-1))
def test_branch_minimum_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="minimum must be non-negative"):
        quota_for_storage(total, weights, minimum=minimum)

# Test for branch: not weights
@given(total=st.integers(min_value=0, max_value=10000),
       minimum=st.integers(min_value=0, max_value=100))
def test_branch_empty_weights(total, minimum):
    with pytest.raises(ValueError, match="no weights provided"):
        quota_for_storage(total, [], minimum=minimum)

# Test for branch: not any(weights)
@given(total=st.integers(min_value=0, max_value=10000),
       minimum=st.integers(min_value=0, max_value=100))
def test_branch_all_zero_weights(total, minimum):
    with pytest.raises(ValueError, match="all weights are zero"):
        quota_for_storage(total, [0, 0, 0], minimum=minimum)

# Test for loop invariant: planned calculation
@given(total=st.integers(min_value=0, max_value=10000),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=0, max_value=100))
def test_loop_invariant_planned_calculation(total, weights, minimum):
    total_weight = sum(weights)
    result = quota_for_storage(total, weights, minimum=minimum)
    for i, allocation in enumerate(result):
        planned_value = max(minimum, (weights[i] / total_weight) * total)
        assert allocation == int(planned_value)

# Test for loop invariant: allocations
@given(total=st.integers(min_value=0, max_value=10000),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=0, max_value=100))
def test_loop_invariant_allocations(total, weights, minimum):
    result = quota_for_storage(total, weights, minimum=minimum)
    for allocation in result:
        assert isinstance(allocation, int)

# Test for return postcondition
@given(total=st.integers(min_value=0, max_value=10000),
       weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
       minimum=st.integers(min_value=0, max_value=100))
def test_return_postcondition(total, weights, minimum):
    result = quota_for_storage(total, weights, minimum=minimum)
    assert len(result) == len(weights)
    total_weight = sum(weights)
    for i, allocation in enumerate(result):
        planned_value = max(minimum, (weights[i] / total_weight) * total)
        assert allocation == int(planned_value)