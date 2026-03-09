import pytest
from hypothesis import given, strategies as st
from datetime import datetime, timedelta

# Assuming the function is in the correct path
from dataset.python_programs.task_throttle import task_throttle

# Property: preserves_length
@given(
    timestamps=st.lists(st.integers(min_value=0), min_size=0, max_size=100),
    now=st.integers(min_value=0, max_value=10000),
    window=st.integers(min_value=1, max_value=10),
    limit=st.integers(min_value=1, max_value=10)
)
def test_preserves_length(timestamps, now, window, limit):
    result = task_throttle(timestamps, now, window=window, limit=limit)
    assert len(result) == 2

# Property: loop_invariant
@given(
    timestamps=st.lists(st.integers(min_value=0), min_size=0, max_size=100),
    now=st.integers(min_value=0, max_value=10000),
    window=st.integers(min_value=1, max_value=10),
    limit=st.integers(min_value=1, max_value=10)
)
def test_loop_invariant(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    for t in recent:
        assert t >= window_start

# Property: branch_specific_behavior
@given(
    timestamps=st.lists(st.integers(min_value=0), min_size=0, max_size=100),
    now=st.integers(min_value=0, max_value=10000),
    window=st.integers(min_value=1, max_value=10),
    limit=st.integers(min_value=1, max_value=10)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    if len(recent) > limit:
        assert task_throttle(timestamps, now, window=window, limit=limit) == (False, 0)
    else:
        assert task_throttle(timestamps, now, window=window, limit=limit) == (True, limit - len(recent))

# Property: return_postcondition
@given(
    timestamps=st.lists(st.integers(min_value=0), min_size=0, max_size=100),
    now=st.integers(min_value=0, max_value=10000),
    window=st.integers(min_value=1, max_value=10),
    limit=st.integers(min_value=1, max_value=10)
)
def test_return_postcondition(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    if len(recent) > limit:
        assert task_throttle(timestamps, now, window=window, limit=limit) == (False, 0)
    else:
        assert task_throttle(timestamps, now, window=window, limit=limit) == (True, limit - len(recent))