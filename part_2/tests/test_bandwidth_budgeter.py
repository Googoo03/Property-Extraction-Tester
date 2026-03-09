import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.bandwidth_budgeter import bandwidth_budgeter

# Property: preserves_length
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
    minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False)
)
def test_preserves_length(total, weights, minimum):
    result = bandwidth_budgeter(total, weights, minimum=minimum)
    assert len(result) == len(weights)

# Property: branch_specific_behavior (total < 0)
@given(
    total=st.integers(max_value=-1),
    weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
    minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False)
)
def test_total_negative_raises(total, weights, minimum):
    with pytest.raises(ValueError):
        bandwidth_budgeter(total, weights, minimum=minimum)

# Property: branch_specific_behavior (minimum < 0)
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
    minimum=st.floats(max_value=-1)
)
def test_minimum_negative_raises(total, weights, minimum):
    with pytest.raises(ValueError):
        bandwidth_budgeter(total, weights, minimum=minimum)

# Property: branch_specific_behavior (not weights)
@given(
    total=st.integers(min_value=0),
    minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False)
)
def test_no_weights_raises(total, minimum):
    with pytest.raises(ValueError):
        bandwidth_budgeter(total, [], minimum=minimum)

# Property: branch_specific_behavior (not any(weights))
@given(
    total=st.integers(min_value=0),
    minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False)
)
def test_all_zero_weights_raises(total, minimum):
    with pytest.raises(ValueError):
        bandwidth_budgeter(total, [0.0, 0.0, 0.0], minimum=minimum)

# Property: loop_invariant (sum(allocations) <= total)
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
    minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False)
)
def test_sum_allocations_leq_total(total, weights, minimum):
    result = bandwidth_budgeter(total, weights, minimum=minimum)
    assert sum(result) <= total

# Property: loop_invariant (all(a >= minimum for a in allocations))
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
    minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False)
)
def test_all_allocations_geq_minimum(total, weights, minimum):
    result = bandwidth_budgeter(total, weights, minimum=minimum)
    assert all(a >= minimum for a in result)

# Property: return_postcondition (all(isinstance(a, int) and a >= minimum for a in allocations))
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
    minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False)
)
def test_all_allocations_are_int_and_geq_minimum(total, weights, minimum):
    result = bandwidth_budgeter(total, weights, minimum=minimum)
    assert all(isinstance(a, int) and a >= minimum for a in result)