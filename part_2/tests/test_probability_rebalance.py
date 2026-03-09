import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.probability_rebalance import probability_rebalance

# Test: preserves_length
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1))
def test_preserves_length(current, target):
    if len(current) == len(target):
        result = probability_rebalance(current, target)
        assert len(result) == len(current)

# Test: branch_specific_behavior (shape mismatch)
@given(current=st.lists(st.floats()), target=st.lists(st.floats()))
def test_raises_value_error_on_shape_mismatch(current, target):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            probability_rebalance(current, target)

# Test: branch_specific_behavior (empty input)
@given(current=st.lists(st.floats(), min_size=0, max_size=0))
def test_raises_value_error_on_empty_input(current):
    target = [0.5]
    with pytest.raises(ValueError):
        probability_rebalance(current, target)

# Test: loop_invariant
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_loop_invariant(current, target, damping):
    if len(current) == len(target):
        result = probability_rebalance(current, target, damping=damping)
        for i, (c, t) in enumerate(zip(current, target)):
            expected = c + (t - c) * damping
            assert abs(result[i] - expected) < 1e-10

# Test: return_postcondition
@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_return_postcondition(current, target, damping):
    if len(current) == len(target):
        result = probability_rebalance(current, target, damping=damping)
        assert result is not None
        assert isinstance(result, list)
        assert len(result) == len(current)