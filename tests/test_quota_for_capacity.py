import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.quota_for_capacity import quota_for_capacity

@given(total=st.floats(allow_nan=False, allow_infinity=False), weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), minimum=st.floats(allow_nan=False, allow_infinity=False))
def test_preserve_length(total, weights, minimum):
    result = quota_for_capacity(total, weights, minimum=minimum)
    assert len(result) == len(weights)

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=0))
def test_empty_weights_raises_value_error(weights):
    with pytest.raises(ValueError):
        quota_for_capacity(10, weights)

@given(total=st.floats(max_value=-0.1, allow_nan=False, allow_infinity=False))
def test_negative_total_raises_value_error(total):
    with pytest.raises(ValueError):
        quota_for_capacity(total, [1.0])

@given(minimum=st.floats(max_value=-0.1, allow_nan=False, allow_infinity=False))
def test_negative_minimum_raises_value_error(minimum):
    with pytest.raises(ValueError):
        quota_for_capacity(10, [1.0], minimum=minimum)

@given(weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_zero_total_weight_raises_value_error(weights):
    with pytest.raises(ValueError):
        quota_for_capacity(10, weights)

@given(total=st.floats(allow_nan=False, allow_infinity=False), weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), minimum=st.floats(allow_nan=False, allow_infinity=False))
def test_loop_invariant_portion_calculation(total, weights, minimum):
    weight_sum = sum(weights)
    shares = []
    for w in weights:
        portion = (w / weight_sum) * total
        shares.append(portion if portion > minimum else minimum)
    result = quota_for_capacity(total, weights, minimum=minimum)
    assert shares == result

@given(total=st.floats(allow_nan=False, allow_infinity=False), weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), minimum=st.floats(allow_nan=False, allow_infinity=False))
def test_floor_to_int_branch(total, weights, minimum):
    result = quota_for_capacity(total, weights, minimum=minimum)
    expected = [int(v) for v in result]
    assert result == expected

@given(total=st.floats(allow_nan=False, allow_infinity=False), weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), minimum=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition_floor_to_int(total, weights, minimum):
    result = quota_for_capacity(total, weights, minimum=minimum)
    assert isinstance(result, list)
    assert all(isinstance(x, int) for x in result)

@given(total=st.floats(allow_nan=False, allow_infinity=False), weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), minimum=st.floats(allow_nan=False, allow_infinity=False))
def test_loop_invariant_semantic_rule(total, weights, minimum):
    weight_sum = sum(weights)
    shares = []
    for w in weights:
        portion = (w / weight_sum) * total
        shares.append(portion if portion > minimum else minimum)
    result = quota_for_capacity(total, weights, minimum=minimum)
    assert shares == result

@given(total=st.floats(allow_nan=False, allow_infinity=False), weights=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), minimum=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition_shares(total, weights, minimum):
    result = quota_for_capacity(total, weights, minimum=minimum)
    assert isinstance(result, list)
    assert all(isinstance(x, (int, float)) for x in result)