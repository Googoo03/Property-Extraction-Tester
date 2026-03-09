import hypothesis
import hypothesis.strategies as st
import pytest
from dataset.python_programs.rolling_usage import rolling_usage

@hypothesis.given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(series):
    window = 5
    warmup_min = 2
    result = rolling_usage(series, window=window, warmup_min=warmup_min)
    assert result is not None

@hypothesis.given(window=st.integers(max_value=0))
def test_branch_specific_behavior_invalid_window(window):
    series = [1.0, 2.0, 3.0, 4.0, 5.0]
    with pytest.raises(ValueError, match="invalid window"):
        rolling_usage(series, window=window, warmup_min=2)

@hypothesis.given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_branch_specific_behavior_empty_series(series):
    with pytest.raises(ValueError, match="no samples"):
        rolling_usage(series, window=5, warmup_min=2)

@hypothesis.given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_warmup(series):
    window = 5
    warmup_min = 10
    result = rolling_usage(series, window=window, warmup_min=warmup_min)
    if len(series) < warmup_min:
        assert result is None
    else:
        assert result is not None

@hypothesis.given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_return_postcondition(series):
    window = 5
    warmup_min = 2
    result = rolling_usage(series, window=window, warmup_min=warmup_min)
    tail = series[-window:]
    if len(tail) < warmup_min:
        assert result is None
    else:
        avg = sum(tail) / window
        assert result == avg

@hypothesis.given(window=st.integers(min_value=1, max_value=100))
def test_valid_window(window):
    series = [1.0, 2.0, 3.0, 4.0, 5.0]
    warmup_min = 2
    result = rolling_usage(series, window=window, warmup_min=warmup_min)
    assert result is not None

@hypothesis.given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_non_empty_series(series):
    window = 5
    warmup_min = 2
    result = rolling_usage(series, window=window, warmup_min=warmup_min)
    assert result is not None

@hypothesis.given(warmup_min=st.integers(min_value=0, max_value=100))
def test_valid_warmup_min(warmup_min):
    series = [1.0, 2.0, 3.0, 4.0, 5.0]
    window = 5
    result = rolling_usage(series, window=window, warmup_min=warmup_min)
    assert result is not None

@hypothesis.given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_average_computation(series):
    window = 5
    warmup_min = 2
    result = rolling_usage(series, window=window, warmup_min=warmup_min)
    tail = series[-window:]
    if len(tail) >= warmup_min:
        avg = sum(tail) / window
        assert result == avg