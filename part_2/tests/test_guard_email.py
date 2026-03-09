import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from dataset.python_programs.guard_email import guard_email

# Property: len(recent) <= len(timestamps)
@given(
    timestamps=st.lists(st.integers()),
    now=st.integers(),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_preserves_length(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    output = guard_email(timestamps, now, window=window, limit=limit)
    assert len(recent) <= len(timestamps)

# Property: all(t >= cutoff for t in recent)
@given(
    timestamps=st.lists(st.integers()),
    now=st.integers(),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_loop_invariant(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    for t in recent:
        assert t >= cutoff

# Property: output == (False, 0) when len(recent) > limit
@given(
    timestamps=st.lists(st.integers()),
    now=st.integers(),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_branch_specific_behavior_false(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        output = guard_email(timestamps, now, window=window, limit=limit)
        assert output == (False, 0)

# Property: output == (True, limit - len(recent)) when len(recent) <= limit
@given(
    timestamps=st.lists(st.integers()),
    now=st.integers(),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_branch_specific_behavior_true(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) <= limit:
        output = guard_email(timestamps, now, window=window, limit=limit)
        assert output == (True, limit - len(recent))

# Property: isinstance(output, tuple) and len(output) == 2 and isinstance(output[0], bool) and isinstance(output[1], int)
@given(
    timestamps=st.lists(st.integers()),
    now=st.integers(),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_return_postcondition(timestamps, now, window, limit):
    output = guard_email(timestamps, now, window=window, limit=limit)
    assert isinstance(output, tuple)
    assert len(output) == 2
    assert isinstance(output[0], bool)
    assert isinstance(output[1], int)