import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.packets_window_avg import packets_window_avg

# Test for 'preserves_length' property
@given(values=st.lists(st.floats()))
def test_preserves_length(values):
    try:
        packets_window_avg(values)
    except ValueError:
        pass

# Test for 'branch_specific_behavior' property where window <= 0
@given(values=st.lists(st.floats()), window=st.integers(max_value=0))
def test_window_less_than_or_equal_zero_raises_value_error(values, window):
    with pytest.raises(ValueError):
        packets_window_avg(values, window=window)

# Test for 'branch_specific_behavior' property where not values
@given(values=st.lists(st.floats(), min_size=0, max_size=0))
def test_empty_values_raises_value_error(values):
    with pytest.raises(ValueError):
        packets_window_avg(values)

# Test for 'branch_specific_behavior' property where len(recent) < warmup_min
@given(values=st.lists(st.floats(), min_size=0, max_size=3), warmup_min=st.integers(min_value=4, max_value=10))
def test_warmup_min_greater_than_length_returns_none(values, warmup_min):
    assert packets_window_avg(values, warmup_min=warmup_min) is None

# Test for 'return_postcondition' property where return is None or instance of int or float
@given(values=st.lists(st.floats()))
def test_return_is_none_or_numeric(values):
    result = packets_window_avg(values)
    assert result is None or isinstance(result, (int, float))

# Test for 'return_postcondition' property where return is None or close to the mean of the last window values
@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1, max_value=10), warmup_min=st.integers(min_value=1, max_value=10))
def test_return_is_none_or_close_to_mean(values, window, warmup_min):
    result = packets_window_avg(values, window=window, warmup_min=warmup_min)
    if result is not None:
        recent = values[-window:]
        expected_mean = sum(recent) / window
        assert abs(result - expected_mean) < 1e-9