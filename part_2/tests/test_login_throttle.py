import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.login_throttle import login_throttle

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1))
def test_preserves_length(timestamps, now, window):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert len(timestamps) == len(recent) + len([t for t in timestamps if t < cutoff])

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1))
def test_loop_invariant(timestamps, now, window):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    assert all(t >= cutoff for t in recent)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    output = login_throttle(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_return_postcondition(timestamps, now, window, limit):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]
    output = login_throttle(timestamps, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(recent))