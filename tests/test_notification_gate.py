import hypothesis
import hypothesis.strategies as st
import pytest
from dataset.python_programs.notification_gate import notification_gate

@hypothesis.given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=1, max_value=10**6)
)
def test_preserves_length(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    assert len(recent) == len([t for t in timestamps if t >= now - window])

@hypothesis.given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=1, max_value=10**6)
)
def test_loop_invariant(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    assert all(t >= window_start for t in recent)

@hypothesis.given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=1, max_value=10**6)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    output = notification_gate(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))

@hypothesis.given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=1, max_value=10**6)
)
def test_return_postcondition(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    output = notification_gate(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))

@hypothesis.given(
    timestamps=st.lists(st.integers(min_value=0, max_value=10**6)),
    now=st.integers(min_value=0, max_value=10**6),
    window=st.integers(min_value=1, max_value=10**6),
    limit=st.integers(min_value=1, max_value=10**6)
)
def test_return_postcondition_boolean(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    output = notification_gate(timestamps, now, window=window, limit=limit)
    assert output[0] == (len(recent) <= limit)