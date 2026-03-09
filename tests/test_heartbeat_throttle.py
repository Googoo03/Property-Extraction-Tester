import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.heartbeat_throttle import heartbeat_throttle

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1e6)),
    now=st.floats(min_value=0, max_value=1e6),
    window=st.floats(min_value=0.1, max_value=100),
    limit=st.integers(min_value=1, max_value=100)
)
def test_preserves_length(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    assert len(timestamps) == len(active) or len(timestamps) > len(active)

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1e6)),
    now=st.floats(min_value=0, max_value=1e6),
    window=st.floats(min_value=0.1, max_value=100),
    limit=st.integers(min_value=1, max_value=100)
)
def test_loop_invariant(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    assert all(t >= cutoff for t in active)

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1e6)),
    now=st.floats(min_value=0, max_value=1e6),
    window=st.floats(min_value=0.1, max_value=100),
    limit=st.integers(min_value=1, max_value=100)
)
def test_branch_specific_behavior(timestamps, now, window, limit):
    output = heartbeat_throttle(timestamps, now, window=window, limit=limit)
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1e6)),
    now=st.floats(min_value=0, max_value=1e6),
    window=st.floats(min_value=0.1, max_value=100),
    limit=st.integers(min_value=1, max_value=100)
)
def test_return_postcondition(timestamps, now, window, limit):
    output = heartbeat_throttle(timestamps, now, window=window, limit=limit)
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))

@given(
    timestamps=st.lists(st.floats(min_value=0, max_value=1e6)),
    now=st.floats(min_value=0, max_value=1e6),
    window=st.floats(min_value=0.1, max_value=100),
    limit=st.integers(min_value=1, max_value=100)
)
def test_return_postcondition_boolean(timestamps, now, window, limit):
    output = heartbeat_throttle(timestamps, now, window=window, limit=limit)
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    if len(active) > limit:
        assert output[0] is False
    else:
        assert output[0] is True