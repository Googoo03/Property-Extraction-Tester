import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.load_rolling_avg import load_rolling_avg

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1, max_value=10), warmup_min=st.integers(min_value=1, max_value=10))
def test_preserve_length(series, window, warmup_min):
    result = load_rolling_avg(series, window=window, warmup_min=warmup_min)
    assert result is not None or len(series) < warmup_min

@given(window=st.integers(max_value=0))
def test_window_leq_zero_raises_value_error(window):
    with pytest.raises(ValueError):
        load_rolling_avg([], window=window, warmup_min=2)

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_empty_series_raises_value_error(series):
    with pytest.raises(ValueError):
        load_rolling_avg(series, window=5, warmup_min=2)

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1, max_value=10), warmup_min=st.integers(min_value=1, max_value=10))
def test_tail_equals_series_last_window(series, window, warmup_min):
    tail = series[-window:]
    assert load_rolling_avg(series, window=window, warmup_min=warmup_min) is None or tail == series[-window:]

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1, max_value=10), warmup_min=st.integers(min_value=1, max_value=10))
def test_correct_average(series, window, warmup_min):
    tail = series[-window:]
    result = load_rolling_avg(series, window=window, warmup_min=warmup_min)
    if result is not None:
        assert result == sum(tail) / window

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1, max_value=10), warmup_min=st.integers(min_value=1, max_value=10))
def test_return_none_when_warmup_min(series, window, warmup_min):
    tail = series[-window:]
    result = load_rolling_avg(series, window=window, warmup_min=warmup_min)
    if len(tail) < warmup_min:
        assert result is None

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1, max_value=10), warmup_min=st.integers(min_value=1, max_value=10))
def test_return_avg_when_warmup_min_met(series, window, warmup_min):
    tail = series[-window:]
    result = load_rolling_avg(series, window=window, warmup_min=warmup_min)
    if len(tail) >= warmup_min:
        assert result == sum(tail) / window

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1, max_value=10), warmup_min=st.integers(min_value=1, max_value=10))
def test_return_type_is_float(series, window, warmup_min):
    result = load_rolling_avg(series, window=window, warmup_min=warmup_min)
    if result is not None:
        assert isinstance(result, float)