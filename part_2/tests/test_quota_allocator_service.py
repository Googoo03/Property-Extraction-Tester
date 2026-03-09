import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.quota_allocator_service import quota_allocator_service

# Test for 'preserves_length' property
@given(
    total=st.integers(min_value=0, max_value=10000),
    weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
    minimum=st.integers(min_value=0, max_value=100)
)
def test_preserves_length(total, weights, minimum):
    result = quota_allocator_service(total, weights, minimum=minimum)
    assert len(result) == len(weights)

# Test for 'branch_specific_behavior' when total < 0
@given(
    total=st.integers(min_value=-10000, max_value=-1),
    weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
    minimum=st.integers(min_value=0, max_value=100)
)
def test_total_negative_raises_value_error(total, weights, minimum):
    with pytest.raises(ValueError, match="total must be non-negative"):
        quota_allocator_service(total, weights, minimum=minimum)

# Test for 'branch_specific_behavior' when minimum < 0
@given(
    total=st.integers(min_value=0, max_value=10000),
    weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
    minimum=st.integers(min_value=-100, max_value=-1)
)
def test_minimum_negative_raises_value_error(total, weights, minimum):
    with pytest.raises(ValueError, match="minimum must be non-negative"):
        quota_allocator_service(total, weights, minimum=minimum)

# Test for 'branch_specific_behavior' when weights are invalid
@given(
    total=st.integers(min_value=0, max_value=10000),
    weights=st.lists(st.integers(min_value=0, max_value=0), min_size=0, max_size=100) | st.lists(st.integers(min_value=1, max_value=100), min_size=0, max_size=0),
    minimum=st.integers(min_value=0, max_value=100)
)
def test_invalid_weights_raises_value_error(weights, total, minimum):
    with pytest.raises(ValueError, match="invalid weights"):
        quota_allocator_service(total, weights, minimum=minimum)

# Test for 'loop_invariant' property regarding raw values
@given(
    total=st.integers(min_value=0, max_value=10000),
    weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
    minimum=st.integers(min_value=0, max_value=100)
)
def test_loop_invariant_raw_values(total, weights, minimum):
    weight_sum = sum(weights)
    raw = [max(minimum, (w / weight_sum) * total) for w in weights]
    assert all(x >= minimum for x in raw) and all(isinstance(x, float) for x in raw)

# Test for 'return_postcondition' property
@given(
    total=st.integers(min_value=0, max_value=10000),
    weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
    minimum=st.integers(min_value=0, max_value=100)
)
def test_return_postcondition(total, weights, minimum):
    result = quota_allocator_service(total, weights, minimum=minimum)
    assert all(isinstance(x, int) for x in result) and all(x >= minimum for x in result)

# Test for 'total_equality' property
@given(
    total=st.integers(min_value=0, max_value=10000),
    weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
    minimum=st.integers(min_value=0, max_value=100)
)
def test_total_equality(total, weights, minimum):
    result = quota_allocator_service(total, weights, minimum=minimum)
    weight_sum = sum(weights)
    assert sum(result) == total or sum(result) == total - (total % weight_sum)

# Test for 'loop_invariant' property regarding sum of raw values
@given(
    total=st.integers(min_value=0, max_value=10000),
    weights=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100),
    minimum=st.integers(min_value=0, max_value=100)
)
def test_loop_invariant_sum_raw_values(total, weights, minimum):
    weight_sum = sum(weights)
    raw = [max(minimum, (w / weight_sum) * total) for w in weights]
    assert sum(raw) == total and all(x >= minimum for x in raw)