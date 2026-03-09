import hypothesis
import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.slots_apportion import slots_apportion

@given(weights=st.lists(st.integers(min_value=1), min_size=1), total=st.integers(min_value=0))
def test_preserves_length(weights, total):
    output = slots_apportion(total, weights)
    assert len(output) == len(weights)

@given(total=st.integers(max_value=-1))
def test_branch_total_negative(total):
    with pytest.raises(ValueError, match="total must be non-negative"):
        slots_apportion(total, [1])

@given(minimum=st.integers(max_value=-1))
def test_branch_minimum_negative(minimum):
    with pytest.raises(ValueError, match="minimum must be non-negative"):
        slots_apportion(0, [1], minimum=minimum)

def test_branch_no_weights():
    with pytest.raises(ValueError, match="no weights provided"):
        slots_apportion(0, [])

def test_branch_all_weights_zero():
    with pytest.raises(ValueError, match="all weights are zero"):
        slots_apportion(0, [0, 0])

@given(weights=st.lists(st.integers(min_value=0), min_size=1), total=st.integers(min_value=0))
def test_loop_invariant_minimum(weights, total):
    minimum = st.integers(min_value=0).example()
    output = slots_apportion(total, weights, minimum=minimum)
    assert all(x >= minimum for x in output)

@given(weights=st.lists(st.integers(min_value=1), min_size=1), total=st.integers(min_value=0))
def test_loop_invariant_sum_leq_total(weights, total):
    output = slots_apportion(total, weights)
    assert sum(output) <= total

@given(weights=st.lists(st.integers(min_value=1), min_size=1), total=st.integers(min_value=0))
def test_return_postcondition(weights, total):
    output = slots_apportion(total, weights)
    assert all(isinstance(x, int) for x in output)