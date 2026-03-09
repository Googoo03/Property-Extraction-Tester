import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.shares_apportion import shares_apportion

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_preserves_length(total, weights, minimum):
    result = shares_apportion(total, weights, minimum=minimum)
    assert len(result) == len(weights)

@given(total=st.integers(max_value=-1), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_branch_total_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="total must be non-negative"):
        shares_apportion(total, weights, minimum=minimum)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(max_value=-1))
def test_branch_minimum_negative(total, weights, minimum):
    with pytest.raises(ValueError, match="minimum must be non-negative"):
        shares_apportion(total, weights, minimum=minimum)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=0), minimum=st.integers(min_value=0))
def test_branch_no_weights(total, weights, minimum):
    with pytest.raises(ValueError, match="no weights provided"):
        shares_apportion(total, weights, minimum=minimum)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=0), min_size=1), minimum=st.integers(min_value=0))
def test_branch_all_weights_zero(total, weights, minimum):
    with pytest.raises(ValueError, match="all weights are zero"):
        shares_apportion(total, weights, minimum=minimum)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_loop_invariant_minimum(total, weights, minimum):
    result = shares_apportion(total, weights, minimum=minimum)
    assert all(x >= minimum for x in result)

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_loop_invariant_sum(total, weights, minimum):
    result = shares_apportion(total, weights, minimum=minimum)
    assert sum(result) <= total

@given(total=st.integers(min_value=0), weights=st.lists(st.integers(min_value=1), min_size=1), minimum=st.integers(min_value=0))
def test_return_postcondition(total, weights, minimum):
    result = shares_apportion(total, weights, minimum=minimum)
    assert isinstance(result, list)
    assert all(isinstance(x, int) for x in result)
    assert all(x >= minimum for x in result)
    assert sum(result) <= total