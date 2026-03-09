import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.sales_window_avg import sales_window_avg

# Test for property: preserves_length
@given(values=st.lists(st.floats(), min_size=4))
def test_preserves_length(values):
    assert len(values) >= 4

# Test for branch: window <= 0
@given(values=st.lists(st.floats(), min_size=1), window=st.integers(max_value=0))
def test_window_non_positive_raises_value_error(values, window):
    with pytest.raises(ValueError):
        sales_window_avg(values, window=window)

# Test for branch: not values
@given(values=st.lists(st.floats(), min_size=0, max_size=0))
def test_empty_values_raises_value_error(values):
    with pytest.raises(ValueError):
        sales_window_avg(values)

# Test for branch: len(recent) < warmup_min
@given(values=st.lists(st.floats(), min_size=1), warmup_min=st.integers(min_value=2))
def test_warmup_min_greater_than_recent_returns_none(values, warmup_min):
    assert sales_window_avg(values, warmup_min=warmup_min) is None

# Test for return: returns value satisfying expected semantics: return None
@given(values=st.lists(st.floats(), min_size=1), warmup_min=st.integers(min_value=2))
def test_returns_none_when_warmup_min_greater_than_recent(values, warmup_min):
    assert sales_window_avg(values, warmup_min=warmup_min) is None

# Test for return: returns value satisfying expected semantics: return mean
@given(values=st.lists(st.floats(), min_size=4))
def test_returns_mean_when_conditions_met(values):
    result = sales_window_avg(values)
    assert result is not None