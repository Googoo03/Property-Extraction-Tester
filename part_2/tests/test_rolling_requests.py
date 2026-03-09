import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.rolling_requests import rolling_requests

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(series):
    result = rolling_requests(series)
    assert result is not None

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_window_zero_raises_value_error(series):
    with pytest.raises(ValueError):
        rolling_requests(series, window=0)

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_empty_series_raises_value_error(series):
    with pytest.raises(ValueError):
        rolling_requests([])

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_warmup_min(series):
    result = rolling_requests(series, warmup_min=len(series) + 1)
    assert result is None

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_return_postcondition_return_none(series):
    result = rolling_requests(series, warmup_min=len(series) + 1)
    assert result is None

@given(series=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_return_postcondition_return_avg(series):
    result = rolling_requests(series)
    assert result is not None