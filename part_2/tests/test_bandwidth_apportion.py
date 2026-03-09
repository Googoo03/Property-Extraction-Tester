import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.bandwidth_apportion import bandwidth_apportion

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_preserves_length(total, weights, minimum):
    output = bandwidth_apportion(total, weights, minimum=minimum)
    assert len(output) == len(weights)

@given(total=st.integers(max_value=-1))
def test_branch_specific_behavior_total_negative(total):
    with pytest.raises(ValueError):
        bandwidth_apportion(total, [1])

@given(minimum=st.integers(max_value=-1))
def test_branch_specific_behavior_minimum_negative(minimum):
    with pytest.raises(ValueError):
        bandwidth_apportion(10, [1], minimum=minimum)

@given(weights=st.lists(st.integers(min_value=0), min_size=0))
def test_branch_specific_behavior_invalid_weights(weights):
    if not weights or sum(weights) == 0:
        with pytest.raises(ValueError):
            bandwidth_apportion(10, weights)
    else:
        bandwidth_apportion(10, weights)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_loop_invariant_minimum(total, weights, minimum):
    total_weight = sum(weights)
    raw = [max(minimum, (w / total_weight) * total) for w in weights]
    assert all(minimum <= x <= total for x in raw)

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_return_postcondition(total, weights, minimum):
    output = bandwidth_apportion(total, weights, minimum=minimum)
    assert all(x >= minimum and x <= total for x in output)
    assert sum(output) <= total

@given(
    total=st.integers(min_value=0),
    weights=st.lists(st.integers(min_value=0), min_size=1),
    minimum=st.integers(min_value=0)
)
def test_loop_invariant_proportionality(total, weights, minimum):
    total_weight = sum(weights)
    raw = [max(minimum, (w / total_weight) * total) for w in weights]
    for w, r in zip(weights, raw):
        if total_weight > 0:
            assert abs((r / total) - (w / total_weight)) < 1e-6