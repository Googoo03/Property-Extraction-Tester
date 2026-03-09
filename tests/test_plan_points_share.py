import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.plan_points_share import plan_points_share

# Property: preserves_length
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_preserves_length(total, weights, minimum):
    output = plan_points_share(total, weights, minimum=minimum)
    assert len(output) == len(weights)

# Property: branch_specific_behavior (total < 0)
@given(
    total=st.integers(max_value=-1),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_branch_total_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="total < 0"):
        plan_points_share(total, weights, minimum=minimum)

# Property: branch_specific_behavior (minimum < 0)
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(max_value=-1)
)
def test_branch_minimum_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="minimum < 0"):
        plan_points_share(total, weights, minimum=minimum)

# Property: branch_specific_behavior (not weights or sum(weights) == 0)
@given(
    total=st.integers(min_value=0),
    minimum=st.integers(min_value=0)
)
def test_branch_invalid_weights(total, minimum):
    with pytest.raises(ValueError, match="invalid weights"):
        plan_points_share(total, [], minimum=minimum)

    with pytest.raises(ValueError, match="invalid weights"):
        plan_points_share(total, [0, 0], minimum=minimum)

# Property: return_postcondition
@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=1), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_return_postcondition(total, weights, minimum):
    output = plan_points_share(total, weights, minimum=minimum)
    weight_sum = sum(weights)
    for w, share in zip(weights, output):
        raw = (w / weight_sum) * total
        assert share == int(raw if raw >= minimum else minimum)