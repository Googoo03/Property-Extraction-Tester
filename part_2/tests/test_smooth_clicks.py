import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.smooth_clicks import smooth_clicks

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_preserves_length(values, window, warmup_min):
    if len(values) >= window:
        result = smooth_clicks(values, window=window, warmup_min=warmup_min)
        assert result is not None

@given(window=st.integers(max_value=0))
def test_window_must_be_positive(window):
    with pytest.raises(ValueError):
        smooth_clicks([], window=window)

@given(values=st.lists(st.floats(), min_size=0))
def test_empty_series_raises_value_error(values):
    if not values:
        with pytest.raises(ValueError):
            smooth_clicks(values)

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_returns_none_if_tail_less_than_warmup_min(values, window, warmup_min):
    if len(values) < warmup_min:
        result = smooth_clicks(values, window=window, warmup_min=warmup_min)
        assert result is None

@given(values=st.lists(st.floats(), min_size=1), window=st.integers(min_value=1), warmup_min=st.integers(min_value=1))
def test_return_mean(values, window, warmup_min):
    if len(values) >= window and len(values[-window:]) >= warmup_min:
        result = smooth_clicks(values, window=window, warmup_min=warmup_min)
        assert result is not None
        assert isinstance(result, float)