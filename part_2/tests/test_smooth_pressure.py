import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.smooth_pressure import smooth_pressure

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_preserves_length(values, window, warmup_min):
    result = smooth_pressure(values, window=window, warmup_min=warmup_min)
    assert result is not None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), warmup_min=st.integers(min_value=1))
def test_branch_window_leq_0_raises_value_error(values, warmup_min):
    with pytest.raises(ValueError):
        smooth_pressure(values, window=0, warmup_min=warmup_min)

@given(window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_branch_not_values_raises_value_error(window, warmup_min):
    with pytest.raises(ValueError):
        smooth_pressure([], window=window, warmup_min=warmup_min)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1))
def test_branch_len_recent_lt_warmup_min_returns_none(values, window):
    warmup_min = len(values[-window:]) + 1
    result = smooth_pressure(values, window=window, warmup_min=warmup_min)
    assert result is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_return_postcondition_returns_none(values, window, warmup_min):
    warmup_min = len(values[-window:]) + 1
    result = smooth_pressure(values, window=window, warmup_min=warmup_min)
    assert result is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_return_postcondition_returns_mean(values, window, warmup_min):
    warmup_min = len(values[-window:]) - 1
    result = smooth_pressure(values, window=window, warmup_min=warmup_min)
    assert result is not None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), warmup_min=st.integers(min_value=1))
def test_exception_raised_window_leq_0(values, warmup_min):
    with pytest.raises(ValueError):
        smooth_pressure(values, window=0, warmup_min=warmup_min)

@given(window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_exception_raised_not_values(window, warmup_min):
    with pytest.raises(ValueError):
        smooth_pressure([], window=window, warmup_min=warmup_min)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_correct_mean_calculation(values, window, warmup_min):
    recent = values[-window:]
    total = sum(recent)
    mean = total / window
    warmup_min = len(values[-window:]) - 1
    result = smooth_pressure(values, window=window, warmup_min=warmup_min)
    assert result == mean

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1))
def test_returns_none(values, window):
    warmup_min = len(values[-window:]) + 1
    result = smooth_pressure(values, window=window, warmup_min=warmup_min)
    assert result is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_returns_mean(values, window, warmup_min):
    warmup_min = len(values[-window:]) - 1
    result = smooth_pressure(values, window=window, warmup_min=warmup_min)
    assert result is not None