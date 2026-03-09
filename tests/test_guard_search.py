import pytest
from hypothesis import given, strategies as st
from datetime import datetime, timedelta
from dataset.python_programs.guard_search import guard_search

# Property: preserves_length
# The length of the output tuple is always 2
@given(
    timestamps=st.lists(st.datetimes(), min_size=0),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=100),
    limit=st.integers(min_value=1, max_value=100)
)
def test_preserves_length(timestamps, now, window, limit):
    result = guard_search(timestamps, now, window=window, limit=limit)
    assert len(result) == 2

# Property: loop_invariant
# The 'active' list should only contain timestamps within the window
@given(
    timestamps=st.lists(st.datetimes(), min_size=0),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=100),
    limit=st.integers(min_value=1, max_value=100)
)
def test_loop_invariant(timestamps, now, window, limit):
    cutoff = now - timedelta(seconds=window)
    result = guard_search(timestamps, now, window=window, limit=limit)
    active = [t for t in timestamps if t >= cutoff]
    _, remaining = result
    assert len(active) == (limit - remaining if result[0] else len(active))

# Property: branch_specific_behavior
# When len(active) > limit, the function returns (False, 0)
@given(
    timestamps=st.lists(st.datetimes(), min_size=6),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=100),
    limit=st.integers(min_value=1, max_value=5)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - timedelta(seconds=window)
    active = [t for t in timestamps if t >= cutoff]
    if len(active) > limit:
        result = guard_search(timestamps, now, window=window, limit=limit)
        assert result == (False, 0)

# Property: return_postcondition (False case)
# When the function returns False, the second element is 0
@given(
    timestamps=st.lists(st.datetimes(), min_size=6),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=100),
    limit=st.integers(min_value=1, max_value=5)
)
def test_return_postcondition_false_case(timestamps, now, window, limit):
    cutoff = now - timedelta(seconds=window)
    active = [t for t in timestamps if t >= cutoff]
    if len(active) > limit:
        result = guard_search(timestamps, now, window=window, limit=limit)
        assert result == (False, 0)

# Property: return_postcondition (True case)
# When the function returns True, the second element is limit - len(active)
@given(
    timestamps=st.lists(st.datetimes(), min_size=0, max_size=5),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=100),
    limit=st.integers(min_value=1, max_value=100)
)
def test_return_postcondition_true_case(timestamps, now, window, limit):
    cutoff = now - timedelta(seconds=window)
    active = [t for t in timestamps if t >= cutoff]
    if len(active) <= limit:
        result = guard_search(timestamps, now, window=window, limit=limit)
        assert result == (True, limit - len(active))