from hypothesis import given
from hypothesis.strategies import lists, floats, sampled_from
import pytest
from dataset.python_programs.traffic_shaping_gate import traffic_shaping_gate

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=1), now=floats(min_value=0, max_value=1e6))
def test_preserves_length(timestamps, now):
    window = 10
    limit = 5
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    assert len(active) == len([t for t in timestamps if t >= now - window])

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=1), now=floats(min_value=0, max_value=1e6))
def test_loop_invariant(timestamps, now):
    window = 10
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    assert all(t >= now - window for t in active)

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=1), now=floats(min_value=0, max_value=1e6))
def test_branch_specific_behavior(timestamps, now):
    window = 10
    limit = 5
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = traffic_shaping_gate(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))

@given(timestamps=lists(floats(min_value=0, max_value=1e6), min_size=1), now=floats(min_value=0, max_value=1e6))
def test_return_postcondition(timestamps, now):
    window = 10
    limit = 5
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]
    output = traffic_shaping_gate(timestamps, now, window=window, limit=limit)
    if len(active) > limit:
        assert output == (False, 0)
    else:
        assert output == (True, limit - len(active))