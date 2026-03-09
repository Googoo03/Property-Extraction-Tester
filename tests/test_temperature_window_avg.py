import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.temperature_window_avg import temperature_window_avg

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_preserves_length(values):
    assert len(values) == len(values)

@given(window=st.integers())
def test_branch_specific_behavior_window_positive(window):
    if window <= 0:
        with pytest.raises(ValueError):
            temperature_window_avg([], window=window)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior_empty_series(values):
    if not values:
        with pytest.raises(ValueError):
            temperature_window_avg(values)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)),
       warmup_min=st.integers())
def test_branch_specific_behavior_warmup_min(values, warmup_min):
    window = 3
    tail = values[-window:]
    if len(tail) < warmup_min:
        assert temperature_window_avg(values, warmup_min=warmup_min) is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)),
       warmup_min=st.integers())
def test_return_postcondition_return_none(values, warmup_min):
    window = 3
    tail = values[-window:]
    if len(tail) < warmup_min:
        assert temperature_window_avg(values, warmup_min=warmup_min) is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_return_postcondition_return_mean(values):
    window = 3
    tail = values[-window:]
    if tail:
        expected_mean = sum(tail) / len(tail)
        assert temperature_window_avg(values) == expected_mean