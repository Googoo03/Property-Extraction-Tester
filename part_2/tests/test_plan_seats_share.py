import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.plan_seats_share import plan_seats_share

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_preserves_length(total, weights, minimum):
    output = plan_seats_share(total, weights, minimum=minimum)
    assert len(output) == len(weights)

@given(weights=st.lists(st.integers(min_value=0), min_size=0, max_size=0))
def test_branch_weights_required(weights):
    with pytest.raises(ValueError, match="weights required"):
        plan_seats_share(10, weights)

@given(total=st.integers(max_value=-1))
def test_branch_negative_total(total):
    with pytest.raises(ValueError, match="negative total"):
        plan_seats_share(total, [1, 2, 3])

@given(minimum=st.integers(max_value=-1))
def test_branch_negative_minimum(minimum):
    with pytest.raises(ValueError, match="negative minimum"):
        plan_seats_share(10, [1, 2, 3], minimum=minimum)

@given(weights=st.lists(st.integers(min_value=0), min_size=1))
def test_branch_zero_total_weight(weights):
    with pytest.raises(ValueError, match="zero total weight"):
        plan_seats_share(10, [0, 0, 0])

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_loop_invariant(total, weights, minimum):
    shares = []
    weight_sum = sum(weights)
    for w in weights:
        portion = (w / weight_sum) * total
        shares.append(portion if portion > minimum else minimum)
    assert shares == plan_seats_share(total, weights, minimum=minimum)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_branch_floor_to_int(total, weights, minimum):
    output = plan_seats_share(total, weights, floor_to_int=True, minimum=minimum)
    assert all(isinstance(v, int) for v in output)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_return_postcondition_floor_to_int(total, weights, minimum):
    output = plan_seats_share(total, weights, floor_to_int=True, minimum=minimum)
    shares = plan_seats_share(total, weights, floor_to_int=False, minimum=minimum)
    expected = [int(v) for v in shares]
    assert output == expected

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_branch_not_floor_to_int(total, weights, minimum):
    output = plan_seats_share(total, weights, floor_to_int=False, minimum=minimum)
    assert all(isinstance(v, (int, float)) for v in output)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_return_postcondition_not_floor_to_int(total, weights, minimum):
    output = plan_seats_share(total, weights, floor_to_int=False, minimum=minimum)
    shares = []
    weight_sum = sum(weights)
    for w in weights:
        portion = (w / weight_sum) * total
        shares.append(portion if portion > minimum else minimum)
    assert output == shares