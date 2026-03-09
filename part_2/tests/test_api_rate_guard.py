import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from dataset.python_programs.api_rate_guard import api_rate_guard

# Property: preserves_length
@given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**9)),
    now=st.integers(min_value=0, max_value=10**9),
    window=st.integers(min_value=1, max_value=10**9)
)
def test_preserves_length(timestamps, now, window):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert len(recent) == len([t for t in timestamps if t >= now - window])

# Property: loop_invariant
@given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**9)),
    now=st.integers(min_value=0, max_value=10**9),
    window=st.integers(min_value=1, max_value=10**9)
)
def test_loop_invariant(timestamps, now, window):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert all(t >= now - window for t in recent)

# Property: branch_specific_behavior
@given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**9)),
    now=st.integers(min_value=0, max_value=10**9),
    window=st.integers(min_value=1, max_value=10**9),
    limit=st.integers(min_value=1, max_value=10**9)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        assert api_rate_guard(timestamps, now, window=window, limit=limit) == (False, 0)
    else:
        assert api_rate_guard(timestamps, now, window=window, limit=limit) == (True, limit - len(recent))

# Property: return_postcondition
@given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**9)),
    now=st.integers(min_value=0, max_value=10**9),
    window=st.integers(min_value=1, max_value=10**9),
    limit=st.integers(min_value=1, max_value=10**9)
)
def test_return_postcondition(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        assert api_rate_guard(timestamps, now, window=window, limit=limit) == (False, 0)
    else:
        assert api_rate_guard(timestamps, now, window=window, limit=limit) == (True, limit - len(recent))