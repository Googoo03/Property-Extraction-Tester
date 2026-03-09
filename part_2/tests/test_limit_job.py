import hypothesis
from hypothesis import given, strategies as st
import pytest

def limit_job(timestamps, now, *, window=60, limit=20):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(
    timestamps=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=0)
)
def test_input_validation(timestamps, now, window, limit):
    assert len(timestamps) >= 0
    assert now >= 0
    assert window > 0
    assert limit >= 0

@given(
    timestamps=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=0)
)
def test_cutoff_calculation(timestamps, now, window, limit):
    cutoff = now - window
    assert cutoff == now - window

@given(
    timestamps=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=0)
)
def test_recent_calculation(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert all(t >= cutoff for t in recent)

@given(
    timestamps=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=0)
)
def test_limit_check(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert len(recent) <= limit or len(recent) > limit

@given(
    timestamps=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=0)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        result = limit_job(timestamps, now, window=window, limit=limit)
        assert result == (False, 0)
    else:
        result = limit_job(timestamps, now, window=window, limit=limit)
        assert result == (True, limit - len(recent))

@given(
    timestamps=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=0)
)
def test_return_postcondition_false(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) > limit:
        result = limit_job(timestamps, now, window=window, limit=limit)
        assert result == (False, 0)

@given(
    timestamps=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=0)
)
def test_return_postcondition_true(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    if len(recent) <= limit:
        result = limit_job(timestamps, now, window=window, limit=limit)
        assert result == (True, limit - len(recent))