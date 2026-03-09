import hypothesis
from hypothesis import given, strategies as st
import pytest

def windowed_error_rate(events, now, *, window=60):
    """
    Compute error rate in a sliding window.
    events: list of (timestamp, is_error)
    """
    cutoff = now - window
    recent = [e for e in events if e[0] >= cutoff]
    if not recent:
        return 0.0

    errors = sum(1 for _, is_err in recent if is_err)
    # BUG: divides by full window length instead of event count.
    return errors / window

@given(
    events=st.lists(st.tuples(st.integers(), st.booleans())),
    now=st.integers(),
    window=st.integers(min_value=1)
)
def test_preserves_length(events, now, window):
    cutoff = now - window
    recent = [e for e in events if e[0] >= cutoff]
    assert len([e for e in events if e[0] >= cutoff]) == len(recent)

@given(
    events=st.lists(st.tuples(st.integers(), st.booleans())),
    now=st.integers(),
    window=st.integers(min_value=1)
)
def test_loop_invariant(events, now, window):
    cutoff = now - window
    recent = [e for e in events if e[0] >= cutoff]
    assert all(e[0] >= (now - window) for e in recent)

@given(
    events=st.lists(st.tuples(st.integers(), st.booleans())),
    now=st.integers(),
    window=st.integers(min_value=1)
)
def test_branch_specific_behavior_no_recent(events, now, window):
    cutoff = now - window
    recent = [e for e in events if e[0] >= cutoff]
    if not recent:
        output = windowed_error_rate(events, now, window=window)
        assert output == 0.0

@given(
    events=st.lists(st.tuples(st.integers(), st.booleans())),
    now=st.integers(),
    window=st.integers(min_value=1)
)
def test_branch_specific_behavior_with_recent(events, now, window):
    cutoff = now - window
    recent = [e for e in events if e[0] >= cutoff]
    if recent:
        output = windowed_error_rate(events, now, window=window)
        errors = sum(1 for _, is_err in recent if is_err)
        assert output == errors / len(recent)

@given(
    events=st.lists(st.tuples(st.integers(), st.booleans())),
    now=st.integers(),
    window=st.integers(min_value=1)
)
def test_return_postcondition(events, now, window):
    cutoff = now - window
    recent = [e for e in events if e[0] >= cutoff]
    output = windowed_error_rate(events, now, window=window)
    if not recent:
        assert output == 0.0
    else:
        errors = sum(1 for _, is_err in recent if is_err)
        assert output == errors / len(recent)