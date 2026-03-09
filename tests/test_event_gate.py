import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.event_gate import event_gate

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1000000), min_size=0, max_size=1000),
    now=st.floats(min_value=0, max_value=1000000),
    window=st.floats(min_value=0.1, max_value=1000000),
    limit=st.integers(min_value=0, max_value=1000)
)
def test_preserves_length(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    left = len(timestamps)
    right = len(recent) + len([t for t in timestamps if t < window_start])
    assert left == right

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1000000), min_size=0, max_size=1000),
    now=st.floats(min_value=0, max_value=1000000),
    window=st.floats(min_value=0.1, max_value=1000000),
    limit=st.integers(min_value=0, max_value=1000)
)
def test_loop_invariant(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    assert all(t >= window_start for t in recent)

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1000000), min_size=0, max_size=1000),
    now=st.floats(min_value=0, max_value=1000000),
    window=st.floats(min_value=0.1, max_value=1000000),
    limit=st.integers(min_value=0, max_value=1000)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    output = event_gate(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1000000), min_size=0, max_size=1000),
    now=st.floats(min_value=0, max_value=1000000),
    window=st.floats(min_value=0.1, max_value=1000000),
    limit=st.integers(min_value=0, max_value=1000)
)
def test_return_postcondition(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    output = event_gate(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1000000), min_size=0, max_size=1000),
    now=st.floats(min_value=0, max_value=1000000),
    window=st.floats(min_value=0.1, max_value=1000000),
    limit=st.integers(min_value=0, max_value=1000)
)
def test_return_postcondition_boolean(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    output = event_gate(timestamps, now, window=window, limit=limit)
    assert output[0] == (len(recent) <= limit)