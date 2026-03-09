import pytest
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays
import numpy as np
from dataset.python_programs.ad_mix import ad_mix

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            ad_mix(current, target, damping=damping)
    else:
        result = ad_mix(current, target, damping=damping)
        assert len(result) == len(current)

@given(current=st.lists(st.floats()), target=st.lists(st.floats()))
def test_branch_specific_behavior_shape_mismatch(current, target):
    if len(current) != len(target):
        with pytest.raises(ValueError, match="shape mismatch"):
            ad_mix(current, target)

@given(current=st.lists(st.floats()), target=st.lists(st.floats()))
def test_branch_specific_behavior_empty_allocation(current, target):
    if not current:
        with pytest.raises(ValueError, match="empty allocation"):
            ad_mix(current, target)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_loop_invariant(current, target, damping):
    if len(current) != len(target):
        return
    result = ad_mix(current, target, damping=damping)
    for i in range(len(current)):
        assert result[i] == current[i] + (target[i] - current[i]) * damping

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_return_postcondition(current, target, damping):
    if len(current) != len(target):
        return
    result = ad_mix(current, target, damping=damping)
    assert isinstance(result, list)
    assert len(result) == len(current)