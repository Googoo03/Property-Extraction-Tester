from hypothesis import given, strategies as st
from dataset.python_programs.download_rate import download_rate

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_preserves_length(timestamps, now, window, limit):
    cutoff = now - window
    left = len(timestamps)
    right = len([t for t in timestamps if t >= cutoff]) + len([t for t in timestamps if t < cutoff])
    assert left == right

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_loop_invariant(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    assert len(active) <= len(timestamps)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = download_rate(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers(min_value=1), limit=st.integers(min_value=1))
def test_return_postcondition(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = download_rate(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))