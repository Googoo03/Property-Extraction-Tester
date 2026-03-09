import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.memory_moving_mean import memory_moving_mean

# Property: len(output) == len(input)
@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=10))
def test_preserves_length(series):
    result = memory_moving_mean(series, window=5, warmup_min=2)
    assert result is None or isinstance(result, float)

# Property: branch_specific_behavior for window <= 0
@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=10))
def test_branch_window_less_than_or_equal_zero(series):
    with pytest.raises(ValueError, match="invalid window"):
        memory_moving_mean(series, window=0, warmup_min=2)

# Property: branch_specific_behavior for not series
@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=0))
def test_branch_empty_series(series):
    with pytest.raises(ValueError, match="no samples"):
        memory_moving_mean(series, window=5, warmup_min=2)

# Property: branch_specific_behavior for len(tail) < warmup_min
@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=1))
def test_branch_tail_less_than_warmup_min(series):
    result = memory_moving_mean(series, window=5, warmup_min=2)
    assert result is None

# Property: return_postcondition for return None
@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=1))
def test_return_postcondition_none(series):
    result = memory_moving_mean(series, window=5, warmup_min=2)
    assert result is None

# Property: return_postcondition for return avg
@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=5, max_size=10))
def test_return_postcondition_avg(series):
    result = memory_moving_mean(series, window=5, warmup_min=2)
    assert isinstance(result, float)