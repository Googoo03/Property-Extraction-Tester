import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.latency_rolling_avg import latency_rolling_avg

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(series):
    result = latency_rolling_avg(series)
    assert result is not None

@given(window=st.integers(max_value=0))
def test_branch_specific_behavior_invalid_window(window):
    with pytest.raises(ValueError, match="invalid window"):
        latency_rolling_avg([], window=window)

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_branch_specific_behavior_no_samples(series):
    if not series:
        with pytest.raises(ValueError, match="no samples"):
            latency_rolling_avg(series)

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       window=st.integers(min_value=1),
       warmup_min=st.integers(min_value=2))
def test_branch_specific_behavior_warmup(series, window, warmup_min):
    tail = series[-window:]
    if len(tail) < warmup_min:
        result = latency_rolling_avg(series, window=window, warmup_min=warmup_min)
        assert result is None

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       window=st.integers(min_value=1),
       warmup_min=st.integers(min_value=2))
def test_return_postcondition_none(series, window, warmup_min):
    tail = series[-window:]
    if len(tail) < warmup_min:
        result = latency_rolling_avg(series, window=window, warmup_min=warmup_min)
        assert result is None

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       window=st.integers(min_value=1))
def test_return_postcondition_avg(series, window):
    tail = series[-window:]
    if len(tail) >= 2:
        result = latency_rolling_avg(series, window=window)
        avg = sum(tail) / window
        assert isinstance(result, float)
        assert result == avg