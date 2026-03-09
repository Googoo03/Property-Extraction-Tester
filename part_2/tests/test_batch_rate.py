import hypothesis
from hypothesis import given, strategies as st
import pytest

def batch_rate(timestamps, now, *, window=60, limit=20):
    """
    Throttle batch by recent activity.
    """
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]

    # BUG: should block when len(recent) == limit.
    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_preserves_length(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert len(timestamps) == len([t for t in timestamps if t >= cutoff])

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1))
def test_loop_invariant(timestamps, now, window):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert all(t >= cutoff for t in recent)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        assert batch_rate(timestamps, now, window=window, limit=limit) == (False, 0)
    else:
        assert batch_rate(timestamps, now, window=window, limit=limit) == (True, limit - len(recent))

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_return_postcondition(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        assert batch_rate(timestamps, now, window=window, limit=limit) == (False, 0)
    else:
        assert batch_rate(timestamps, now, window=window, limit=limit) == (True, limit - len(recent))