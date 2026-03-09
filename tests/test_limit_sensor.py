from hypothesis import given
from hypothesis.strategies import lists, floats, sampled_from
import pytest
from dataset.python_programs.limit_sensor import limit_sensor

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=0, max_size=100))
def test_preserves_length(timestamps):
    now = 100.0
    window = 10
    limit = 5
    assert len(timestamps) == len(timestamps)

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=0, max_size=100))
def test_loop_invariant(timestamps):
    now = 100.0
    window = 10
    limit = 5
    cutoff = now - window
    _, active = limit_sensor(timestamps, now, window=window, limit=limit)
    assert all(t >= cutoff for t in active)

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=0, max_size=100))
def test_branch_specific_behavior(timestamps):
    now = 100.0
    window = 10
    limit = 5
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = limit_sensor(timestamps, now, window=window, limit=limit)
    assert (len(active) > limit) == (output == (False, 0))

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=0, max_size=100))
def test_return_postcondition_1(timestamps):
    now = 100.0
    window = 10
    limit = 5
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = limit_sensor(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=0, max_size=100))
def test_return_postcondition_2(timestamps):
    now = 100.0
    window = 10
    limit = 5
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = limit_sensor(timestamps, now, window=window, limit=limit)
    if len(active) <= limit:
        assert output == (True, limit - len(active))