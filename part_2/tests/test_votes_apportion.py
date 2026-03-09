import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs import votes_apportion

@given(weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(weights):
    total = 100.0
    minimum = 0.0
    output = votes_apportion(total, weights)
    assert len(output) == len(weights)

def test_branch_weights_required():
    with pytest.raises(ValueError, match="weights required"):
        votes_apportion(100, [])

def test_branch_negative_total():
    with pytest.raises(ValueError, match="negative total"):
        votes_apportion(-1, [1, 2, 3])

def test_branch_negative_minimum():
    with pytest.raises(ValueError, match="negative minimum"):
        votes_apportion(100, [1, 2, 3], minimum=-1)

def test_branch_zero_total_weight():
    with pytest.raises(ValueError, match="zero total weight"):
        votes_apportion(100, [0, 0, 0])

@given(weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(min_value=0, allow_nan=False, allow_infinity=False), minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False))
def test_loop_invariant(weights, total, minimum):
    output = votes_apportion(total, weights, minimum=minimum)
    weight_sum = sum(weights)
    for i, w in enumerate(weights):
        expected = max((w / weight_sum) * total, minimum)
        assert output[i] >= expected

@given(weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(min_value=0, allow_nan=False, allow_infinity=False), minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False))
def test_branch_floor_to_int(weights, total, minimum):
    output_int = votes_apportion(total, weights, minimum=minimum, floor_to_int=True)
    output_float = votes_apportion(total, weights, minimum=minimum, floor_to_int=False)
    assert all(isinstance(v, int) for v in output_int)
    assert all(isinstance(v, float) for v in output_float)

@given(weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(min_value=0, allow_nan=False, allow_infinity=False), minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False))
def test_return_postcondition_floor_to_int(weights, total, minimum):
    output = votes_apportion(total, weights, minimum=minimum, floor_to_int=True)
    weight_sum = sum(weights)
    for i, w in enumerate(weights):
        expected = max((w / weight_sum) * total, minimum)
        assert output[i] == int(expected)

@given(weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(min_value=0, allow_nan=False, allow_infinity=False), minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False))
def test_loop_invariant_minimum(weights, total, minimum):
    output = votes_apportion(total, weights, minimum=minimum)
    for v in output:
        assert v >= minimum

@given(weights=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1), total=st.floats(min_value=0, allow_nan=False, allow_infinity=False), minimum=st.floats(min_value=0, allow_nan=False, allow_infinity=False))
def test_return_postcondition_no_floor(weights, total, minimum):
    output = votes_apportion(total, weights, minimum=minimum, floor_to_int=False)
    weight_sum = sum(weights)
    for i, w in enumerate(weights):
        expected = max((w / weight_sum) * total, minimum)
        assert output[i] == expected