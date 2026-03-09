import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.water_allocator import water_allocator

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(weights):
    total = 100
    output = water_allocator(total, weights)
    assert len(output) == len(weights)

@given(total=st.floats(allow_nan=False, allow_infinity=False))
def test_branch_specific_behavior_weights_required(total):
    with pytest.raises(ValueError, match="weights required"):
        water_allocator(total, [])

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_negative_total(weights):
    with pytest.raises(ValueError, match="negative total"):
        water_allocator(-1, weights)

@given(total=st.floats(allow_nan=False, allow_infinity=False), weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_negative_minimum(total, weights):
    with pytest.raises(ValueError, match="negative minimum"):
        water_allocator(total, weights, minimum=-1)

@given(total=st.floats(allow_nan=False, allow_infinity=False))
def test_branch_specific_behavior_zero_total_weight(total):
    with pytest.raises(ValueError, match="zero total weight"):
        water_allocator(total, [0, 0, 0])

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(allow_nan=False, allow_infinity=False))
def test_loop_invariant_minimum(weights, total):
    output = water_allocator(total, weights)
    assert all(v >= 0 for v in output)

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(allow_nan=False, allow_infinity=False))
def test_branch_specific_behavior_floor_to_int(weights, total):
    output = water_allocator(total, weights, floor_to_int=True)
    assert all(isinstance(v, int) for v in output)

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition_type(weights, total):
    output = water_allocator(total, weights, floor_to_int=True)
    assert all(isinstance(v, int) for v in output)
    output = water_allocator(total, weights, floor_to_int=False)
    assert all(isinstance(v, float) for v in output)

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(allow_nan=False, allow_infinity=False))
def test_loop_invariant_sum_approximation(weights, total):
    output = water_allocator(total, weights)
    assert sum(output) <= total + len(weights) * 0

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition_minimum(weights, total):
    output = water_allocator(total, weights)
    assert all(v >= 0 for v in output)