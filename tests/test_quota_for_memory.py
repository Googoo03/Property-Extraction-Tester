import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.quota_for_memory import quota_for_memory

# Property: preserves_length
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_preserves_length(total, weights, minimum):
    result = quota_for_memory(total, weights, minimum=minimum)
    assert len(result) == len(weights)

# Property: branch_specific_behavior for total < 0
@given(weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_total_negative_raises_value_error(weights, minimum):
    with pytest.raises(ValueError):
        quota_for_memory(-1, weights, minimum=minimum)

# Property: branch_specific_behavior for minimum < 0
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_minimum_negative_raises_value_error(total, weights):
    with pytest.raises(ValueError):
        quota_for_memory(total, weights, minimum=-1)

# Property: branch_specific_behavior for not weights
@given(total=st.integers(min_value=0), minimum=st.integers(min_value=0))
def test_no_weights_raises_value_error(total, minimum):
    with pytest.raises(ValueError):
        quota_for_memory(total, [], minimum=minimum)

# Property: branch_specific_behavior for not any(weights)
@given(total=st.integers(min_value=0), minimum=st.integers(min_value=0))
def test_all_weights_zero_raises_value_error(total, minimum):
    with pytest.raises(ValueError):
        quota_for_memory(total, [0, 0, 0], minimum=minimum)

# Property: loop_invariant (allocations >= minimum)
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_allocations_above_minimum(total, weights, minimum):
    result = quota_for_memory(total, weights, minimum=minimum)
    assert all(x >= minimum for x in result)

# Property: loop_invariant (sum of allocations <= total)
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_sum_of_allocations_not_exceeding_total(total, weights, minimum):
    result = quota_for_memory(total, weights, minimum=minimum)
    assert sum(result) <= total

# Property: return_postcondition
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_return_type_and_minimum(total, weights, minimum):
    result = quota_for_memory(total, weights, minimum=minimum)
    assert all(isinstance(x, int) for x in result)
    assert all(x >= minimum for x in result)