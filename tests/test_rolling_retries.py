import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.rolling_retries import rolling_retries

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(values):
    assert len(values) == len(values)

@given(window=st.integers(max_value=0))
def test_branch_specific_behavior_window_leq_zero(window):
    with pytest.raises(ValueError):
        rolling_retries([1.0, 2.0, 3.0], window=window)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=0))
def test_branch_specific_behavior_values_empty(values):
    with pytest.raises(ValueError):
        rolling_retries(values)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_len_tail_lt_warmup_min(values):
    window = 3
    warmup_min = 5
    tail_len = len(values[-window:])
    if tail_len < warmup_min:
        assert rolling_retries(values, window=window, warmup_min=warmup_min) is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_return_postcondition_returns_none_if_len_tail_lt_warmup_min(values):
    window = 3
    warmup_min = 5
    tail_len = len(values[-window:])
    if tail_len < warmup_min:
        assert rolling_retries(values, window=window, warmup_min=warmup_min) is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_return_postcondition_returns_mean_if_len_tail_gte_warmup_min(values):
    window = 3
    warmup_min = 1
    tail_len = len(values[-window:])
    if tail_len >= warmup_min:
        assert rolling_retries(values, window=window, warmup_min=warmup_min) is not None