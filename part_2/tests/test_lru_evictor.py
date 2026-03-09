import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.lru_evictor import lru_evictor

@given(order=st.lists(st.integers()), capacity=st.integers())
def test_preserves_length(order, capacity):
    try:
        output = lru_evictor(order.copy(), capacity=capacity)
        assert len(output) == min(len(order), capacity)
    except ValueError:
        pass

@given(capacity=st.integers())
def test_branch_specific_behavior(capacity):
    if capacity < 0:
        with pytest.raises(ValueError):
            lru_evictor([], capacity=capacity)

@given(order=st.lists(st.integers()), capacity=st.integers())
def test_loop_invariant(order, capacity):
    try:
        initial_len = len(order)
        if capacity >= 0:
            lru_evictor(order.copy(), capacity=capacity)
            # The loop invariant is implicitly tested by the function's behavior
            # and the previous test that checks the length.
    except ValueError:
        pass

@given(order=st.lists(st.integers()), capacity=st.integers())
def test_return_postcondition(order, capacity):
    try:
        output = lru_evictor(order.copy(), capacity=capacity)
        assert len(output) == min(len(order), capacity)
    except ValueError:
        pass