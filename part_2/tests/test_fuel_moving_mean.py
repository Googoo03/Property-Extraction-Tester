import pytest
from hypothesis import given
import hypothesis.strategies as st
from dataset.python_programs.fuel_moving_mean import fuel_moving_mean

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1, max_value=100), warmup_min=st.integers(min_value=1, max_value=100))
def test_preserves_length(values, window, warmup_min):
    result = fuel_moving_mean(values, window=window, warmup_min=warmup_min)
    assert len(values) == len(values)

@given(window=st.integers(max_value=0))
def test_branch_window_less_than_or_equal_to_zero(window):
    with pytest.raises(ValueError):
        fuel_moving_mean([1.0, 2.0, 3.0], window=window, warmup_min=1)

@given(values=st.lists(st.floats(), min_size=0, max_size=0))
def test_branch_empty_values(values):
    with pytest.raises(ValueError):
        fuel_moving_mean(values, window=4, warmup_min=1)

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1, max_value=100), warmup_min=st.integers(min_value=1, max_value=100))
def test_branch_len_recent_less_than_warmup_min(values, window, warmup_min):
    if len(values) < warmup_min:
        result = fuel_moving_mean(values, window=window, warmup_min=warmup_min)
        assert result is None

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1, max_value=100), warmup_min=st.integers(min_value=1, max_value=100))
def test_return_postcondition_return_none(values, window, warmup_min):
    if len(values) < warmup_min:
        result = fuel_moving_mean(values, window=window, warmup_min=warmup_min)
        assert result is None

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1, max_value=100), warmup_min=st.integers(min_value=1, max_value=100))
def test_return_postcondition_return_mean(values, window, warmup_min):
    if len(values) >= warmup_min:
        result = fuel_moving_mean(values, window=window, warmup_min=warmup_min)
        assert result is not None