import pytest
from hypothesis import given, strategies as st
import numpy as np

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            from dataset.python_programs.shift_traffic import shift_traffic
            shift_traffic(current, target, damping=damping)
    else:
        from dataset.python_programs.shift_traffic import shift_traffic
        output = shift_traffic(current, target, damping=damping)
        assert len(output) == len(current)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_branch_specific_behavior_shape_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            from dataset.python_programs.shift_traffic import shift_traffic
            shift_traffic(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=0), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_branch_specific_behavior_empty_allocation(current, target, damping):
    if not current:
        with pytest.raises(ValueError, match="empty allocation"):
            from dataset.python_programs.shift_traffic import shift_traffic
            shift_traffic(current, target, damping=damping)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_loop_invariant(current, target, damping):
    if len(current) == len(target) and current:
        from dataset.python_programs.shift_traffic import shift_traffic
        output = shift_traffic(current, target, damping=damping)
        for idx in range(len(current)):
            assert np.isclose(output[idx], current[idx] + (target[idx] - current[idx]) * damping)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_return_postcondition(current, target, damping):
    if len(current) == len(target) and current:
        from dataset.python_programs.shift_traffic import shift_traffic
        output = shift_traffic(current, target, damping=damping)
        for idx in range(len(current)):
            assert np.isclose(output[idx], current[idx] + (target[idx] - current[idx]) * damping)