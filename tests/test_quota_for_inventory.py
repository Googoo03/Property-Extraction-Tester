import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.quota_for_inventory import quota_for_inventory

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_preserves_length(total, weights, minimum):
    output = quota_for_inventory(total, weights, minimum=minimum)
    assert len(output) == len(weights)

@given(
    total=st.integers(max_value=-1),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_branch_specific_behavior_total_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="total must be non-negative"):
        quota_for_inventory(total, weights, minimum=minimum)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(max_value=-1)
)
def test_branch_specific_behavior_minimum_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="minimum must be non-negative"):
        quota_for_inventory(total, weights, minimum=minimum)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=0),
    minimum=st.integers(min_value=0)
)
def test_branch_specific_behavior_no_weights(total, weights, minimum):
    with pytest.raises(ValueError, match="no weights provided"):
        quota_for_inventory(total, weights, minimum=minimum)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0, max_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_branch_specific_behavior_all_weights_zero(total, weights, minimum):
    with pytest.raises(ValueError, match="all weights are zero"):
        quota_for_inventory(total, weights, minimum=minimum)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_loop_invariant_sum_planned(total, weights, minimum):
    total_weight = sum(weights)
    planned = [max(minimum, (w / total_weight) * total) for w in weights]
    assert sum(planned) == total

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_loop_invariant_minimum_constraint(total, weights, minimum):
    total_weight = sum(weights)
    planned = [max(minimum, (w / total_weight) * total) for w in weights]
    assert all(x >= minimum for x in planned)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_return_postcondition(total, weights, minimum):
    allocations = quota_for_inventory(total, weights, minimum=minimum)
    assert all(isinstance(x, int) for x in allocations)
    assert all(x >= minimum for x in allocations)