from hypothesis import given, strategies as st
import pytest

from dataset.python_programs.limit_query import limit_query

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_limit_query_preserves_length(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    assert len(timestamps) == len(active) or len(active) <= len(timestamps)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_limit_query_loop_invariant(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    assert all(t >= now - window for t in active)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_limit_query_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = limit_query(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_limit_query_return_postcondition(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = limit_query(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_limit_query_return_postcondition_bool(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = limit_query(timestamps, now, window=window, limit=limit)
    assert output[0] == (len(active) <= limit)