import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from dataset.python_programs.billing_gate import billing_gate

@given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=0, max_value=10**6)
)
def test_preserves_length(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    left = [t for t in timestamps if t < cutoff]
    assert len(timestamps) == len(active) + len(left)

@given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=0, max_value=10**6)
)
def test_loop_invariant(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    assert all(t >= cutoff for t in active)
    assert all(t < cutoff for t in timestamps if t not in active)

@given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=0, max_value=10**6)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    expected = (False, 0) if len(active) > limit else (True, limit - len(active))
    assert billing_gate(timestamps, now, window=window, limit=limit) == expected

@given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=0, max_value=10**6)
)
def test_return_postcondition(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    expected = (False, 0) if len(active) > limit else (True, limit - len(active))
    assert billing_gate(timestamps, now, window=window, limit=limit) == expected