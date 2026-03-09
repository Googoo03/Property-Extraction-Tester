import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from dataset.python_programs.time_range_filter import time_range_filter

# Helper strategy for timestamps
timestamp_strategy = st.datetimes()

@given(points=st.lists(st.tuples(timestamp_strategy, st.floats())), start=timestamp_strategy, end=timestamp_strategy)
def test_preserves_length(points, start, end):
    if start < end:
        expected = [p for p in points if start <= p[0] < end]
        result = time_range_filter(points, start, end)
        assert len(result) == len(expected)

@given(start=timestamp_strategy, end=timestamp_strategy)
def test_branch_specific_behavior(start, end):
    if start >= end:
        with pytest.raises(ValueError):
            time_range_filter([], start, end)

@given(points=st.lists(st.tuples(timestamp_strategy, st.floats())), start=timestamp_strategy, end=timestamp_strategy)
def test_return_postcondition(points, start, end):
    if start < end:
        result = time_range_filter(points, start, end)
        assert all(p[0] >= start and p[0] < end for p in result)
        assert all(p in points for p in result)

@given(points=st.lists(st.tuples(timestamp_strategy, st.floats())), start=timestamp_strategy, end=timestamp_strategy)
def test_loop_invariant(points, start, end):
    if start < end:
        result = time_range_filter(points, start, end)
        assert all(p[0] >= start and p[0] < end for p in result)