import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.scores_apportion import scores_apportion

# Property: preserves_length
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_preserves_length(total, weights):
    result = scores_apportion(total, weights)
    assert len(result) == len(weights)

# Property: branch_specific_behavior (total < 0)
@given(weights=st.lists(st.integers(min_value=1), min_size=1))
def test_branch_total_negative(weights):
    with pytest.raises(ValueError, match="total < 0"):
        scores_apportion(-1, weights)

# Property: branch_specific_behavior (minimum < 0)
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_branch_minimum_negative(total, weights):
    with pytest.raises(ValueError, match="minimum < 0"):
        scores_apportion(total, weights, minimum=-1)

# Property: branch_specific_behavior (not weights or sum(weights) == 0)
def test_branch_invalid_weights():
    with pytest.raises(ValueError, match="invalid weights"):
        scores_apportion(10, [])
    with pytest.raises(ValueError, match="invalid weights"):
        scores_apportion(10, [0, 0])

# Property: sum_conservation
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_sum_conservation(total, weights):
    result = scores_apportion(total, weights)
    assert sum(result) <= total

# Property: minimum_bound
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_minimum_bound(total, weights, minimum):
    result = scores_apportion(total, weights, minimum=minimum)
    assert all(x >= minimum for x in result)

# Property: weights_proportionality
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_weights_proportionality(total, weights):
    result = scores_apportion(total, weights)
    weight_sum = sum(weights)
    expected_sum = sum((w / weight_sum) * total for w in weights)
    assert abs(expected_sum - sum(result)) <= total * 1e-6

# Property: return_postcondition
@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1))
def test_return_postcondition(total, weights):
    result = scores_apportion(total, weights)
    weight_sum = sum(weights)
    shares = [(w / weight_sum) * total if (w / weight_sum) * total >= 0 else 0 for w in weights]
    expected = [int(share) for share in shares]
    assert result == expected