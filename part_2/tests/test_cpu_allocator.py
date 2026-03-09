import hypothesis
import hypothesis.strategies as st
import pytest
from dataset.python_programs.cpu_allocator import cpu_allocator

@st.composite
def total_weights_minimum_strategy(draw):
    total = draw(st.integers(min_value=0, max_value=10000))
    weights = draw(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=100))
    minimum = draw(st.integers(min_value=0, max_value=1000))
    return total, weights, minimum

@hypothesis.given(total_weights_minimum_strategy())
def test_preserves_length(total, weights, minimum):
    output = cpu_allocator(total, weights, minimum=minimum)
    assert len(output) == len(weights)

@hypothesis.given(total=st.integers(max_value=-1))
def test_branch_total_negative_raises_value_error(total):
    weights = [1, 2, 3]
    with pytest.raises(ValueError):
        cpu_allocator(total, weights)

@hypothesis.given(minimum=st.integers(max_value=-1))
def test_branch_minimum_negative_raises_value_error(minimum):
    total = 10
    weights = [1, 2, 3]
    with pytest.raises(ValueError):
        cpu_allocator(total, weights, minimum=minimum)

@hypothesis.given(total=st.integers(min_value=0, max_value=1000))
def test_branch_empty_weights_raises_value_error(total):
    weights = []
    with pytest.raises(ValueError):
        cpu_allocator(total, weights)

@hypothesis.given(total=st.integers(min_value=0, max_value=1000))
def test_branch_all_weights_zero_raises_value_error(total):
    weights = [0, 0, 0]
    with pytest.raises(ValueError):
        cpu_allocator(total, weights)

@hypothesis.given(total_weights_minimum_strategy())
def test_loop_invariant_all_above_minimum(total, weights, minimum):
    allocations = cpu_allocator(total, weights, minimum=minimum)
    assert all(x >= minimum for x in allocations)

@hypothesis.given(total_weights_minimum_strategy())
def test_loop_invariant_sum_leq_total(total, weights, minimum):
    allocations = cpu_allocator(total, weights, minimum=minimum)
    assert sum(allocations) <= total

@hypothesis.given(total_weights_minimum_strategy())
def test_return_postcondition_all_integers(total, weights, minimum):
    allocations = cpu_allocator(total, weights, minimum=minimum)
    assert all(isinstance(x, int) for x in allocations)