import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.sensor_window_avg import sensor_window_avg

@given(samples=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1), min_samples=st.integers(min_value=1))
def test_validates_input(samples, window, min_samples):
    result = sensor_window_avg(samples, window=window, min_samples=min_samples)
    assert isinstance(result, float)

@given(samples=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), min_samples=st.integers(min_value=1))
def test_raises_error_on_non_positive_window(samples, min_samples):
    with pytest.raises(ValueError):
        sensor_window_avg(samples, window=0, min_samples=min_samples)

@given(window=st.integers(min_value=1), min_samples=st.integers(min_value=1))
def test_raises_error_on_empty_samples(window, min_samples):
    with pytest.raises(ValueError):
        sensor_window_avg([], window=window, min_samples=min_samples)

@given(samples=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1))
def test_returns_none_when_fewer_samples_than_min_samples(samples, window):
    min_samples = window + 1
    result = sensor_window_avg(samples, window=window, min_samples=min_samples)
    assert result is None

@given(samples=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1), min_samples=st.integers(min_value=1))
def test_returns_mean(samples, window, min_samples):
    if len(samples) >= min_samples:
        result = sensor_window_avg(samples, window=window, min_samples=min_samples)
        assert isinstance(result, float)
        assert result == sum(samples[-window:]) / window