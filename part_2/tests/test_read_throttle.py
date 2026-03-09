import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.read_throttle import read_throttle

@given(timestamps=st.lists(st.floats(min_value=0)), now=st.floats(min_value=0))
def test_preserves_length(timestamps, now):
    window = 10
    assert len(timestamps) == len([t for t in timestamps if t >= now - window]) or len(timestamps) > len([t for t in timestamps if t >= now - window])

@given(timestamps=st.lists(st.floats(min_value=0)), now=st.floats(min_value=0))
def test_loop_invariant(timestamps, now):
    window = 10
    active = [t for t in timestamps if t >= now - window]
    assert all(t >= now - window for t in active)

@given(timestamps=st.lists(st.floats(min_value=0)), now=st.floats(min_value=0))
def test_branch_specific_behavior(timestamps, now):
    window = 10
    limit = 5
    active = [t for t in timestamps if t >= now - window]
    output = read_throttle(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))

@given(timestamps=st.lists(st.floats(min_value=0)), now=st.floats(min_value=0))
def test_return_postcondition_1(timestamps, now):
    window = 10
    limit = 5
    active = [t for t in timestamps if t >= now - window]
    output = read_throttle(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))

@given(timestamps=st.lists(st.floats(min_value=0)), now=st.floats(min_value=0))
def test_return_postcondition_2(timestamps, now):
    window = 10
    limit = 5
    active = [t for t in timestamps if t >= now - window]
    output = read_throttle(timestamps, now, window=window, limit=limit)
    assert output[0] == (len(active) <= limit)