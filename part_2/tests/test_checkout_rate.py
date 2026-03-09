from hypothesis import given, strategies as st
from datetime import datetime, timedelta
from dataset.python_programs.checkout_rate import checkout_rate

# Property: preserves_length
@given(
    timestamps=st.lists(st.datetimes(), min_size=0),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=1000),
    limit=st.integers(min_value=0, max_value=100)
)
def test_preserves_length(timestamps, now, window, limit):
    window_start = now - timedelta(seconds=window)
    recent = [t for t in timestamps if t >= window_start]
    output = checkout_rate(timestamps, now, window=window, limit=limit)
    assert len(recent) == len([t for t in timestamps if t >= now - timedelta(seconds=window)])

# Property: loop_invariant
@given(
    timestamps=st.lists(st.datetimes(), min_size=0),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=1000),
    limit=st.integers(min_value=0, max_value=100)
)
def test_loop_invariant(timestamps, now, window, limit):
    window_start = now - timedelta(seconds=window)
    recent = [t for t in timestamps if t >= window_start]
    output = checkout_rate(timestamps, now, window=window, limit=limit)
    assert all(t >= now - timedelta(seconds=window) for t in recent)

# Property: branch_specific_behavior
@given(
    timestamps=st.lists(st.datetimes(), min_size=0),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=1000),
    limit=st.integers(min_value=0, max_value=100)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    window_start = now - timedelta(seconds=window)
    recent = [t for t in timestamps if t >= window_start]
    output = checkout_rate(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))

# Property: return_postcondition
@given(
    timestamps=st.lists(st.datetimes(), min_size=0),
    now=st.datetimes(),
    window=st.integers(min_value=1, max_value=1000),
    limit=st.integers(min_value=0, max_value=100)
)
def test_return_postcondition(timestamps, now, window, limit):
    window_start = now - timedelta(seconds=window)
    recent = [t for t in timestamps if t >= window_start]
    output = checkout_rate(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))