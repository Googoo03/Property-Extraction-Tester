import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.budget_budgeter import budget_budgeter

# Property: preserves_length
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_preserves_length(total, weights):
    result = budget_budgeter(total, weights)
    assert len(result) == len(weights)

# Property: branch_specific_behavior (total < 0)
@given(weights=st.lists(st.integers(min_value=1), min_size=1))
def test_branch_total_negative(weights):
    with pytest.raises(ValueError, match="total must be non-negative"):
        budget_budgeter(-1, weights)

# Property: branch_specific_behavior (minimum < 0)
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_branch_minimum_negative(total, weights):
    with pytest.raises(ValueError, match="minimum must be non-negative"):
        budget_budgeter(total, weights, minimum=-1)

# Property: branch_specific_behavior (not weights)
def test_branch_no_weights():
    with pytest.raises(ValueError, match="no weights provided"):
        budget_budgeter(10, [])

# Property: branch_specific_behavior (not any(weights))
@given(total=st.integers(min_value=0))
def test_branch_all_weights_zero(total):
    with pytest.raises(ValueError, match="all weights are zero"):
        budget_budgeter(total, [0, 0, 0])

# Property: loop_invariant (all x >= minimum)
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_loop_invariant_minimum(total, weights, minimum):
    result = budget_budgeter(total, weights, minimum=minimum)
    assert all(x >= minimum for x in result)

# Property: loop_invariant (sum(allocations) <= total)
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_loop_invariant_sum(total, weights):
    result = budget_budgeter(total, weights)
    assert sum(result) <= total

# Property: return_postcondition (all isinstance(x, int) for x in allocations)
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_return_postcondition(total, weights):
    result = budget_budgeter(total, weights)
    assert all(isinstance(x, int) for x in result)