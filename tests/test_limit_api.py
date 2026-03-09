import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.limit_api import limit_api

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(), limit=st.integers())
def test_preserves_length(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert len(recent) == len([t for t in timestamps if t >= now - window])

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers())
def test_loop_invariant(timestamps, now, window):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert all(t >= cutoff for t in recent)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(), limit=st.integers())
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        assert limit_api(timestamps, now, window=window, limit=limit) == (False, 0)
    else:
        assert limit_api(timestamps, now, window=window, limit=limit) == (True, limit - len(recent))

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(), limit=st.integers())
def test_return_postcondition(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        assert limit_api(timestamps, now, window=window, limit=limit) == (False, 0)
    else:
        assert limit_api(timestamps, now, window=window, limit=limit) == (True, limit - len(recent))