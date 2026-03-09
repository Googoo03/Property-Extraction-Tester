import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.plan_tickets_share import plan_tickets_share

# Property: preserves_length
@given(weights=st.lists(st.floats(min_value=0.0, max_value=1e6), min_size=1), total=st.floats(min_value=0.0, max_value=1e6), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_preserves_length(weights, total, minimum):
    output = plan_tickets_share(total, weights, minimum=minimum)
    assert len(output) == len(weights)

# Property: branch_specific_behavior (len(weights) == 0)
@given(total=st.floats(min_value=0.0, max_value=1e6), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_branch_weights_required(total, minimum):
    with pytest.raises(ValueError, match="weights required"):
        plan_tickets_share(total, [], minimum=minimum)

# Property: branch_specific_behavior (total < 0)
@given(weights=st.lists(st.floats(min_value=0.0, max_value=1e6), min_size=1), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_branch_negative_total(weights, minimum):
    with pytest.raises(ValueError, match="negative total"):
        plan_tickets_share(-1.0, weights, minimum=minimum)

# Property: branch_specific_behavior (minimum < 0)
@given(weights=st.lists(st.floats(min_value=0.0, max_value=1e6), min_size=1), total=st.floats(min_value=0.0, max_value=1e6))
def test_branch_negative_minimum(weights, total):
    with pytest.raises(ValueError, match="negative minimum"):
        plan_tickets_share(total, weights, minimum=-1.0)

# Property: branch_specific_behavior (sum(weights) == 0)
@given(total=st.floats(min_value=0.0, max_value=1e6), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_branch_zero_total_weight(total, minimum):
    with pytest.raises(ValueError, match="zero total weight"):
        plan_tickets_share(total, [0.0, 0.0], minimum=minimum)

# Property: loop_invariant (portion calculation)
@given(weights=st.lists(st.floats(min_value=0.0, max_value=1e6), min_size=1), total=st.floats(min_value=0.0, max_value=1e6), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_loop_invariant_portion(weights, total, minimum):
    weight_sum = sum(weights)
    output = plan_tickets_share(total, weights, minimum=minimum)
    for w, portion in zip(weights, output):
        expected_portion = (w / weight_sum) * total
        assert portion == expected_portion if expected_portion > minimum else minimum

# Property: branch_specific_behavior (floor_to_int)
@given(weights=st.lists(st.floats(min_value=0.0, max_value=1e6), min_size=1), total=st.floats(min_value=0.0, max_value=1e6), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_branch_floor_to_int(weights, total, minimum):
    output = plan_tickets_share(total, weights, minimum=minimum, floor_to_int=True)
    shares = []
    weight_sum = sum(weights)
    for w in weights:
        portion = (w / weight_sum) * total
        shares.append(portion if portion > minimum else minimum)
    expected_output = [int(v) for v in shares]
    assert output == expected_output

# Property: return_postcondition (floor_to_int)
@given(weights=st.lists(st.floats(min_value=0.0, max_value=1e6), min_size=1), total=st.floats(min_value=0.0, max_value=1e6), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_return_postcondition_floor_to_int(weights, total, minimum):
    output = plan_tickets_share(total, weights, minimum=minimum, floor_to_int=True)
    assert all(isinstance(v, int) for v in output)

# Property: loop_invariant (iteration preserves semantic rule)
@given(weights=st.lists(st.floats(min_value=0.0, max_value=1e6), min_size=1), total=st.floats(min_value=0.0, max_value=1e6), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_loop_invariant_iteration(weights, total, minimum):
    weight_sum = sum(weights)
    output = plan_tickets_share(total, weights, minimum=minimum, floor_to_int=False)
    for w, portion in zip(weights, output):
        expected_portion = (w / weight_sum) * total
        assert portion == expected_portion if expected_portion > minimum else minimum

# Property: return_postcondition (shares)
@given(weights=st.lists(st.floats(min_value=0.0, max_value=1e6), min_size=1), total=st.floats(min_value=0.0, max_value=1e6), minimum=st.floats(min_value=0.0, max_value=1e6))
def test_return_postcondition_shares(weights, total, minimum):
    output = plan_tickets_share(total, weights, minimum=minimum, floor_to_int=False)
    weight_sum = sum(weights)
    for w, portion in zip(weights, output):
        expected_portion = (w / weight_sum) * total
        assert portion == expected_portion if expected_portion > minimum else minimum