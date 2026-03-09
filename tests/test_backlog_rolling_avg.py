import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.backlog_rolling_avg import backlog_rolling_avg

# Test for property: preserves_length (len(values) >= 0)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_preserves_length(values):
    backlog_rolling_avg(values)

# Test for branch: window <= 0 (raises ValueError)
@given(window=st.integers(max_value=0))
def test_branch_window_non_positive(window):
    with pytest.raises(ValueError):
        backlog_rolling_avg([1, 2, 3], window=window)

# Test for branch: not values (raises ValueError)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_branch_empty_values(values):
    if not values:
        with pytest.raises(ValueError):
            backlog_rolling_avg(values)

# Test for branch: len(recent) < warmup_min (returns None)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       warmup_min=st.integers(min_value=2))
def test_branch_warmup_not_met(values, warmup_min):
    result = backlog_rolling_avg(values, warmup_min=warmup_min)
    if len(values) < warmup_min:
        assert result is None

# Test for return: returns None when len(recent) < warmup_min
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       warmup_min=st.integers(min_value=2))
def test_return_none_when_warmup_not_met(values, warmup_min):
    if len(values) < warmup_min:
        result = backlog_rolling_avg(values, warmup_min=warmup_min)
        assert result is None

# Test for return: returns mean when len(recent) >= warmup_min
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       warmup_min=st.integers(min_value=1))
def test_return_mean_when_warmup_met(values, warmup_min):
    if len(values) >= warmup_min:
        result = backlog_rolling_avg(values, warmup_min=warmup_min)
        assert result is not None
        assert isinstance(result, float)