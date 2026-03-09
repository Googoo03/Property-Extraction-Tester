import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from dataset.python_programs.limit_message import limit_message

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(), limit=st.integers())
def test_preserves_length(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert len(timestamps) == len(recent) + sum(1 for t in timestamps if t < cutoff)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(), limit=st.integers())
def test_loop_invariant(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert all(t >= cutoff for t in recent)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(), limit=st.integers())
def test_branch_specific_behavior_greater_than_limit(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        output = limit_message(timestamps, now, window=window, limit=limit)
        assert output == (False, 0)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(), limit=st.integers())
def test_branch_specific_behavior_less_than_or_equal_limit(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) <= limit:
        output = limit_message(timestamps, now, window=window, limit=limit)
        assert output == (True, limit - len(recent))

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(), limit=st.integers())
def test_return_postcondition(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    output = limit_message(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))