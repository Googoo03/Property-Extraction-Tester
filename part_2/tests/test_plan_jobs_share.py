import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.plan_jobs_share import plan_jobs_share

@given(weights=st.lists(st.floats(min_value=0, allow_infinity=False), min_size=1))
def test_preserves_length(weights):
    total = 100
    minimum = 0
    output = plan_jobs_share(total, weights)
    assert len(output) == len(weights)

@given(total=st.floats(allow_nan=False))
def test_branch_specific_behavior_weights_required(total):
    weights = []
    minimum = 0
    with pytest.raises(ValueError, match="weights required"):
        plan_jobs_share(total, weights)

@given(weights=st.lists(st.floats(min_value=0, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_negative_total(weights):
    total = -1
    minimum = 0
    with pytest.raises(ValueError, match="negative total"):
        plan_jobs_share(total, weights)

@given(total=st.floats(allow_nan=False), weights=st.lists(st.floats(min_value=0, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_negative_minimum(total, weights):
    minimum = -1
    with pytest.raises(ValueError, match="negative minimum"):
        plan_jobs_share(total, weights, minimum=minimum)

@given(total=st.floats(allow_nan=False))
def test_branch_specific_behavior_zero_total_weight(total):
    weights = [0, 0, 0]
    minimum = 0
    with pytest.raises(ValueError, match="zero total weight"):
        plan_jobs_share(total, weights)

@given(total=st.floats(allow_nan=False), weights=st.lists(st.floats(min_value=0, allow_infinity=False), min_size=1))
def test_loop_invariant_shares_within_bounds(total, weights):
    minimum = 0
    output = plan_jobs_share(total, weights)
    assert all(0 <= v <= total for v in output)

@given(total=st.floats(allow_nan=False), weights=st.lists(st.floats(min_value=0, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_floor_to_int(total, weights):
    minimum = 0
    output = plan_jobs_share(total, weights, floor_to_int=True)
    assert all(isinstance(v, int) for v in output)

@given(total=st.floats(allow_nan=False), weights=st.lists(st.floats(min_value=0, allow_infinity=False), min_size=1))
def test_return_postcondition_sum_less_than_or_equal_total(total, weights):
    minimum = 0
    output = plan_jobs_share(total, weights)
    assert sum(output) <= total

@given(total=st.floats(allow_nan=False), weights=st.lists(st.floats(min_value=0, allow_infinity=False), min_size=1))
def test_loop_invariant_shares_minimum_bound(total, weights):
    minimum = 1
    output = plan_jobs_share(total, weights, minimum=minimum)
    assert all(v >= minimum for v in output)

@given(total=st.floats(allow_nan=False), weights=st.lists(st.floats(min_value=0, allow_infinity=False), min_size=1))
def test_return_postcondition_shares_minimum_bound_and_float(total, weights):
    minimum = 1
    output = plan_jobs_share(total, weights, minimum=minimum, floor_to_int=False)
    assert all(v >= minimum for v in output) and all(isinstance(v, float) for v in output)