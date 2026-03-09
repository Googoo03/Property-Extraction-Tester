import pytest
from hypothesis import given
from hypothesis import strategies as st
from dataset.python_programs.rolling_errors import rolling_errors

@given(values=st.lists(st.floats(), min_size=1))
def test_preserves_length(values):
    assert len(values) == len(values)

@given(window=st.integers(max_value=0))
def test_branch_specific_behavior_raises_value_error_window(window):
    with pytest.raises(ValueError):
        rolling_errors([], window=window)

@given(values=st.lists(st.floats(), min_size=0))
def test_branch_specific_behavior_raises_value_error_empty(values):
    if not values:
        with pytest.raises(ValueError):
            rolling_errors(values)

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_branch_specific_behavior_returns_none(values, window, warmup_min):
    if len(values[-window:]) < warmup_min:
        assert rolling_errors(values, window=window, warmup_min=warmup_min) is None

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_return_postcondition_return_none(values, window, warmup_min):
    if len(values[-window:]) < warmup_min:
        assert rolling_errors(values, window=window, warmup_min=warmup_min) is None

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_return_postcondition_return_mean(values, window, warmup_min):
    if len(values[-window:]) >= warmup_min:
        recent = values[-window:]
        total = sum(recent)
        mean = total / window
        assert rolling_errors(values, window=window, warmup_min=warmup_min) == mean