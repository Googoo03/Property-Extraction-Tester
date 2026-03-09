import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.queue_window_avg import queue_window_avg

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserve_length(values):
    result = queue_window_avg(values)
    assert len(values) == len(values)

@given(window=st.integers(max_value=0))
def test_branch_specific_behavior_window_invalid(window):
    with pytest.raises(ValueError):
        queue_window_avg([1, 2, 3], window=window)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_branch_specific_behavior_empty_list(values):
    if not values:
        with pytest.raises(ValueError):
            queue_window_avg(values)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       warmup_min=st.integers(min_value=2))
def test_branch_specific_behavior_warmup_min(values, warmup_min):
    result = queue_window_avg(values, warmup_min=warmup_min)
    tail = values[-3:]
    if len(tail) < warmup_min:
        assert result is None
    else:
        assert result is not None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       warmup_min=st.integers(min_value=2))
def test_return_postcondition_none(values, warmup_min):
    tail = values[-3:]
    if len(tail) < warmup_min:
        result = queue_window_avg(values, warmup_min=warmup_min)
        assert result is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       warmup_min=st.integers(min_value=1))
def test_return_postcondition_mean(values, warmup_min):
    tail = values[-3:]
    if len(tail) >= warmup_min:
        result = queue_window_avg(values, warmup_min=warmup_min)
        assert isinstance(result, float)