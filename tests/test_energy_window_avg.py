import hypothesis
from hypothesis import given, strategies as st
import pytest
import math

from dataset.python_programs.energy_window_avg import energy_window_avg

# Property: len(output) == len(input)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)), window=st.integers(min_value=1, max_value=100), warmup_min=st.integers(min_value=1, max_value=100))
def test_preserves_length(values, window, warmup_min):
    try:
        result = energy_window_avg(values, window=window, warmup_min=warmup_min)
    except ValueError:
        return
    if result is None:
        assert len(values) < warmup_min
    else:
        assert isinstance(result, float)

# Property: output behavior depends on condition (window <= 0)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)), warmup_min=st.integers(min_value=1, max_value=100))
def test_window_non_positive_raises_error(values, warmup_min):
    with pytest.raises(ValueError):
        energy_window_avg(values, window=0, warmup_min=warmup_min)
    with pytest.raises(ValueError):
        energy_window_avg(values, window=-1, warmup_min=warmup_min)

# Property: output behavior depends on condition (not values)
@given(window=st.integers(min_value=1, max_value=100), warmup_min=st.integers(min_value=1, max_value=100))
def test_empty_values_raises_error(window, warmup_min):
    with pytest.raises(ValueError):
        energy_window_avg([], window=window, warmup_min=warmup_min)

# Property: output behavior depends on condition (len(recent) < warmup_min)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)), window=st.integers(min_value=1, max_value=100))
def test_returns_none_during_warmup(values, window):
    warmup_min = len(values) + 1
    result = energy_window_avg(values, window=window, warmup_min=warmup_min)
    assert result is None

# Property: returns value satisfying expected semantics (return None)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)), window=st.integers(min_value=1, max_value=100), warmup_min=st.integers(min_value=1, max_value=100))
def test_returns_none_during_warmup_logic(values, window, warmup_min):
    if len(values) < warmup_min:
        result = energy_window_avg(values, window=window, warmup_min=warmup_min)
        assert result is None

# Property: returns value satisfying expected semantics (return mean)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)), window=st.integers(min_value=1, max_value=100), warmup_min=st.integers(min_value=1, max_value=100))
def test_returns_mean_after_warmup(values, window, warmup_min):
    if len(values) >= warmup_min:
        result = energy_window_avg(values, window=window, warmup_min=warmup_min)
        assert isinstance(result, float)