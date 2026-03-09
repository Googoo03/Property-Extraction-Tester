import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.smooth_cpu import smooth_cpu

# Test for 'preserves_length' property
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)), window=st.integers(min_value=1))
def test_preserves_length(values, window):
    if len(values) >= window:
        result = smooth_cpu(values, window=window)
        assert result is not None

# Test for 'branch_specific_behavior' property: window <= 0
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)), window=st.integers(max_value=0))
def test_window_non_positive_raises_value_error(values, window):
    with pytest.raises(ValueError):
        smooth_cpu(values, window=window)

# Test for 'branch_specific_behavior' property: not values
@given(window=st.integers(min_value=1))
def test_empty_values_raises_value_error(window):
    with pytest.raises(ValueError):
        smooth_cpu([], window=window)

# Test for 'branch_specific_behavior' property: len(tail) < warmup_min
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=1), warmup_min=st.integers(min_value=1))
def test_warmup_min_greater_than_tail_length_returns_none(values, warmup_min):
    result = smooth_cpu(values, warmup_min=warmup_min)
    assert result is None

# Test for 'return_postcondition' property: returns None
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=1), warmup_min=st.integers(min_value=1))
def test_returns_none_when_warmup_min_greater_than_tail_length(values, warmup_min):
    if len(values) < warmup_min:
        result = smooth_cpu(values, warmup_min=warmup_min)
        assert result is None

# Test for 'return_postcondition' property: returns mean
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=3), window=st.integers(min_value=1, max_value=2), warmup_min=st.integers(min_value=1))
def test_returns_correct_mean(values, window, warmup_min):
    if len(values) >= window and len(values[-window:]) >= warmup_min:
        result = smooth_cpu(values, window=window, warmup_min=warmup_min)
        assert result is not None
        tail = values[-window:]
        expected_mean = sum(tail) / len(tail)
        assert result == expected_mean