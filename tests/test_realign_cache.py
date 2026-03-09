import pytest
from hypothesis import given
from hypothesis import strategies as st
from dataset.python_programs.realign_cache import realign_cache

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1))
def test_realign_cache_preserves_length(current, target):
    output = realign_cache(current, target)
    assert len(output) == len(current)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1))
def test_realign_cache_branch_specific_behavior_shape_mismatch(current, target):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            realign_cache(current, target)

@given(current=st.lists(st.floats(), min_size=0), target=st.lists(st.floats(), min_size=1))
def test_realign_cache_branch_specific_behavior_empty_current(current, target):
    if not current:
        with pytest.raises(ValueError):
            realign_cache(current, target)

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1), damping=st.floats())
def test_realign_cache_loop_invariant(current, target, damping):
    if len(current) == len(target):
        adjusted = realign_cache(current, target, damping=damping)
        for i in range(len(current)):
            assert adjusted[i] == current[i] + (target[i] - current[i]) * damping

@given(current=st.lists(st.floats(), min_size=1), target=st.lists(st.floats(), min_size=1))
def test_realign_cache_return_postcondition(current, target):
    adjusted = realign_cache(current, target)
    assert adjusted is not None
    assert all(isinstance(x, float) for x in adjusted)