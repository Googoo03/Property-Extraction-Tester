import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.guard_write import guard_write

@given(timestamps=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_preserves_length(timestamps):
    now = 0
    window = 5
    limit = 3
    assert len(timestamps) == len(timestamps)

@given(timestamps=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       now=st.floats(allow_nan=False, allow_infinity=False),
       window=st.floats(allow_nan=False, allow_infinity=False, min_value=0))
def test_loop_invariant(timestamps, now, window):
    limit = 3
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    assert len(recent) <= limit

@given(timestamps=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       now=st.floats(allow_nan=False, allow_infinity=False),
       window=st.floats(allow_nan=False, allow_infinity=False, min_value=0),
       limit=st.integers(min_value=0))
def test_branch_specific_behavior_when_len_recent_greater_than_limit(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    if len(recent) > limit:
        output = guard_write(timestamps, now, window=window, limit=limit)
        assert output == (False, 0)

@given(timestamps=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       now=st.floats(allow_nan=False, allow_infinity=False),
       window=st.floats(allow_nan=False, allow_infinity=False, min_value=0),
       limit=st.integers(min_value=0))
def test_branch_specific_behavior_when_len_recent_less_than_or_equal_to_limit(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    if len(recent) <= limit:
        output = guard_write(timestamps, now, window=window, limit=limit)
        assert output == (True, limit - len(recent))

@given(timestamps=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       now=st.floats(allow_nan=False, allow_infinity=False),
       window=st.floats(allow_nan=False, allow_infinity=False, min_value=0),
       limit=st.integers(min_value=0))
def test_return_postcondition(timestamps, now, window, limit):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]
    if len(recent) > limit:
        output = guard_write(timestamps, now, window=window, limit=limit)
        assert output == (False, 0)
    else:
        output = guard_write(timestamps, now, window=window, limit=limit)
        assert output == (True, limit - len(recent))