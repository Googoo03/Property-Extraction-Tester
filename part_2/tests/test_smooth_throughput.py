import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.smooth_throughput import smooth_throughput

@given(series=st.lists(st.floats(), min_size=1))
def test_valid_window(series):
    result = smooth_throughput(series, window=5)
    assert isinstance(result, (float, type(None)))

@given(series=st.lists(st.floats(), min_size=1))
def test_non_empty_series(series):
    result = smooth_throughput(series, window=5)
    assert isinstance(result, (float, type(None)))

def test_raises_value_error_invalid_window():
    with pytest.raises(ValueError, match="invalid window"):
        smooth_throughput([], window=0)

def test_raises_value_error_no_samples():
    with pytest.raises(ValueError, match="no samples"):
        smooth_throughput([], window=5)

@given(series=st.lists(st.floats(), min_size=1))
def test_returns_none(series):
    result = smooth_throughput(series, window=5, warmup_min=10)
    assert result is None

@given(series=st.lists(st.floats(), min_size=1))
def test_return_postcondition(series):
    result = smooth_throughput(series, window=5)
    assert result is None or isinstance(result, float)

@given(series=st.lists(st.floats(), min_size=1))
def test_correct_average(series):
    result = smooth_throughput(series, window=5)
    if result is not None:
        assert result == sum(series[-5:]) / 5