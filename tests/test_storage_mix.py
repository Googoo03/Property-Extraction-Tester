import pytest
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays
from dataset.python_programs.storage_mix import storage_mix

@given(
    current=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=100),
    target=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=100),
    damping=st.floats(min_value=0, max_value=1)
)
def test_preserve_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            storage_mix(current, target, damping=damping)
    else:
        result = storage_mix(current, target, damping=damping)
        assert len(result) == len(current)

@given(
    current=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=100),
    target=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=100),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_specific_behavior_length_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            storage_mix(current, target, damping=damping)

@given(
    current=st.lists(st.floats(min_value=0, max_value=1), min_size=0, max_size=0),
    target=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_specific_behavior_empty_current(current, target, damping):
    with pytest.raises(ValueError):
        storage_mix(current, target, damping=damping)

@given(
    current=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=100),
    target=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=100),
    damping=st.floats(min_value=0, max_value=1)
)
def test_loop_invariant(current, target, damping):
    if len(current) != len(target):
        return
    if not current:
        return
    result = storage_mix(current, target, damping=damping)
    if all(0 <= c <= 1 and 0 <= t <= 1 for c, t in zip(current, target)):
        assert all(0 <= adjusted <= 1 for adjusted in result)

@given(
    current=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=100),
    target=st.lists(st.floats(min_value=0, max_value=1), min_size=1, max_size=100),
    damping=st.floats(min_value=0, max_value=1)
)
def test_return_postcondition(current, target, damping):
    if len(current) != len(target):
        return
    if not current:
        return
    result = storage_mix(current, target, damping=damping)
    assert sum(result) == sum(current) + damping * (sum(target) - sum(current))