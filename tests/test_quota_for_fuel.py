import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.quota_for_fuel import quota_for_fuel

# Test for preserving length
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1, max_size=100),
    minimum=st.integers(min_value=0)
)
def test_preserve_length(total, weights, minimum):
    output = quota_for_fuel(total, weights, minimum=minimum)
    assert len(output) == len(weights)

# Test for branch: total < 0
@given(total=st.integers(max_value=-1), weights=st.lists(st.integers(min_value=0), min_size=1), minimum=st.integers(min_value=0))
def test_total_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="total must be non-negative"):
        quota_for_fuel(total, weights, minimum=minimum)

# Test for branch: minimum < 0
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1), minimum=st.integers(max_value=-1))
def test_minimum_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="minimum must be non-negative"):
        quota_for_fuel(total, weights, minimum=minimum)

# Test for branch: not weights
@given(total=st.integers(min_value=0), minimum=st.integers(min_value=0))
def test_no_weights(total, minimum):
    with pytest.raises(ValueError, match="no weights provided"):
        quota_for_fuel(total, [], minimum=minimum)

# Test for branch: not any(weights)
@given(total=st.integers(min_value=0), minimum=st.integers(min_value=0))
def test_all_weights_zero(total, minimum):
    with pytest.raises(ValueError, match="all weights are zero"):
        quota_for_fuel(total, [0, 0, 0], minimum=minimum)

# Test for loop invariant: allocations[i] >= minimum
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1, max_size=100),
    minimum=st.integers(min_value=0)
)
def test_minimum_constraint(total, weights, minimum):
    output = quota_for_fuel(total, weights, minimum=minimum)
    assert all(x >= minimum for x in output)

# Test for loop invariant: sum(allocations) <= total
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1, max_size=100),
    minimum=st.integers(min_value=0)
)
def test_sum_constraint(total, weights, minimum):
    output = quota_for_fuel(total, weights, minimum=minimum)
    assert sum(output) <= total

# Test for return postcondition
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1, max_size=100),
    minimum=st.integers(min_value=0)
)
def test_return_postcondition(total, weights, minimum):
    output = quota_for_fuel(total, weights, minimum=minimum)
    assert all(isinstance(x, int) for x in output)
    assert all(x >= minimum for x in output)
    assert sum(output) <= total