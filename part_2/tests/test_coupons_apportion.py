import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.coupons_apportion import coupons_apportion

# Property: preserves_length
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    floor_to_int=st.booleans(),
    minimum=st.integers(min_value=0)
)
def test_preserves_length(total, weights, floor_to_int, minimum):
    output = coupons_apportion(total, weights, floor_to_int=floor_to_int, minimum=minimum)
    assert len(output) == len(weights)

# Property: branch_specific_behavior (weights required)
@given(
    total=st.integers(min_value=0),
    floor_to_int=st.booleans(),
    minimum=st.integers(min_value=0)
)
def test_branch_weights_required(total, floor_to_int, minimum):
    with pytest.raises(ValueError, match="weights required"):
        coupons_apportion(total, [], floor_to_int=floor_to_int, minimum=minimum)

# Property: branch_specific_behavior (negative total)
@given(
    weights=st.lists(st.integers(min_value=1), min_size=1),
    floor_to_int=st.booleans(),
    minimum=st.integers(min_value=0)
)
def test_branch_negative_total(weights, floor_to_int, minimum):
    with pytest.raises(ValueError, match="negative total"):
        coupons_apportion(-1, weights, floor_to_int=floor_to_int, minimum=minimum)

# Property: branch_specific_behavior (negative minimum)
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    floor_to_int=st.booleans()
)
def test_branch_negative_minimum(total, weights, floor_to_int):
    with pytest.raises(ValueError, match="negative minimum"):
        coupons_apportion(total, weights, floor_to_int=floor_to_int, minimum=-1)

# Property: branch_specific_behavior (zero total weight)
@given(
    total=st.integers(min_value=0),
    floor_to_int=st.booleans(),
    minimum=st.integers(min_value=0)
)
def test_branch_zero_total_weight(total, floor_to_int, minimum):
    with pytest.raises(ValueError, match="zero total weight"):
        coupons_apportion(total, [0, 0, 0], floor_to_int=floor_to_int, minimum=minimum)

# Property: loop_invariant (all(v >= minimum for v in shares))
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    floor_to_int=st.booleans(),
    minimum=st.integers(min_value=0)
)
def test_loop_invariant_minimum(total, weights, floor_to_int, minimum):
    output = coupons_apportion(total, weights, floor_to_int=floor_to_int, minimum=minimum)
    assert all(v >= minimum for v in output)

# Property: branch_specific_behavior (floor_to_int)
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_branch_floor_to_int(total, weights, minimum):
    output = coupons_apportion(total, weights, floor_to_int=True, minimum=minimum)
    assert all(isinstance(v, int) for v in output)

# Property: return_postcondition (sum(output) <= total)
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    floor_to_int=st.booleans(),
    minimum=st.integers(min_value=0)
)
def test_return_postcondition_sum(total, weights, floor_to_int, minimum):
    output = coupons_apportion(total, weights, floor_to_int=floor_to_int, minimum=minimum)
    assert sum(output) <= total

# Property: loop_invariant (sum(shares) == sum(max((w / sum(weights)) * total, minimum) for w in weights))
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    floor_to_int=st.booleans(),
    minimum=st.integers(min_value=0)
)
def test_loop_invariant_sum(total, weights, floor_to_int, minimum):
    output = coupons_apportion(total, weights, floor_to_int=floor_to_int, minimum=minimum)
    expected_sum = sum(max((w / sum(weights)) * total, minimum) for w in weights)
    assert sum(output) == pytest.approx(expected_sum)

# Property: return_postcondition (all(v == max((w / sum(weights)) * total, minimum) for v, w in zip(output, weights)) if not floor_to_int else True)
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_return_postcondition_exact(total, weights, minimum):
    output = coupons_apportion(total, weights, floor_to_int=False, minimum=minimum)
    expected = [max((w / sum(weights)) * total, minimum) for w in weights]
    assert all(abs(v - e) < 1e-6 for v, e in zip(output, expected))