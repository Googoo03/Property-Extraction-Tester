import pytest
from hypothesis import given
import hypothesis.strategies as st
from dataset.python_programs.adjust_queue import adjust_queue

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_preserves_length(current, target, damping):
    if len(current) == len(target):
        output = adjust_queue(current, target, damping=damping)
        assert len(output) == len(current)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=2),
       damping=st.floats(min_value=0, max_value=1))
def test_branch_specific_behavior_shape_mismatch(current, target, damping):
    with pytest.raises(ValueError):
        adjust_queue(current, target, damping=damping)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       damping=st.floats(min_value=0, max_value=1))
def test_branch_specific_behavior_empty_allocation(current, target, damping):
    if not current:
        with pytest.raises(ValueError):
            adjust_queue(current, target, damping=damping)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_loop_invariant(current, target, damping):
    if len(current) == len(target):
        output = adjust_queue(current, target, damping=damping)
        assert all(abs(output[i] - (current[i] + (target[i] - current[i]) * damping)) < 1e-9 for i in range(len(current)))

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_return_postcondition(current, target, damping):
    if len(current) == len(target):
        output = adjust_queue(current, target, damping=damping)
        assert all(abs(output[i] - (current[i] + (target[i] - current[i]) * damping)) < 1e-9 for i in range(len(current)))