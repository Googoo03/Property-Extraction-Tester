import hypothesis
from hypothesis import given, strategies as st
from datetime import datetime, timedelta

# Assuming the function is in the specified path
from dataset.python_programs.upload_gate import upload_gate

# Property: preserves_length - This property checks that the length of the output tuple is always 2
@given(timestamps=st.lists(st.floats()), now=st.floats(), window=st.floats(), limit=st.integers())
def test_preserves_length(timestamps, now, window, limit):
    result = upload_gate(timestamps, now, window=window, limit=limit)
    assert len(result) == 2

# Property: loop_invariant - This property checks that the filtering of timestamps is correct
@given(timestamps=st.lists(st.floats()), now=st.floats(), window=st.floats(), limit=st.integers())
def test_loop_invariant(timestamps, now, window, limit):
    cutoff = now - window
    result = upload_gate(timestamps, now, window=window, limit=limit)
    active = [t for t in timestamps if t >= cutoff]
    expected_result = (len(active) <= limit, max(0, limit - len(active)))
    assert result == expected_result

# Property: branch_specific_behavior - This property checks the behavior when len(active) > limit
@given(timestamps=st.lists(st.floats()), now=st.floats(), window=st.floats(), limit=st.integers())
def test_branch_specific_behavior(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    if len(active) > limit:
        result = upload_gate(timestamps, now, window=window, limit=limit)
        assert result == (False, 0)

# Property: return_postcondition - This property checks the return value when the condition is False
@given(timestamps=st.lists(st.floats()), now=st.floats(), window=st.floats(), limit=st.integers())
def test_return_postcondition_false(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    if len(active) > limit:
        result = upload_gate(timestamps, now, window=window, limit=limit)
        assert result == (False, 0)

# Property: return_postcondition - This property checks the return value when the condition is True
@given(timestamps=st.lists(st.floats()), now=st.floats(), window=st.floats(), limit=st.integers())
def test_return_postcondition_true(timestamps, now, window, limit):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    if len(active) <= limit:
        result = upload_gate(timestamps, now, window=window, limit=limit)
        assert result == (True, limit - len(active))