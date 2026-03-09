import pytest
from hypothesis import given
from hypothesis import strategies as st
from dataset.python_programs.volume_moving_mean import volume_moving_mean

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_volume_moving_mean_preserves_length(values):
    result = volume_moving_mean(values)
    assert result is not None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), window=st.integers(max_value=0))
def test_volume_moving_mean_branch_specific_behavior_window(values, window):
    with pytest.raises(ValueError):
        volume_moving_mean(values, window=window)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_volume_moving_mean_branch_specific_behavior_empty(values):
    with pytest.raises(ValueError):
        volume_moving_mean(values)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), warmup_min=st.integers(max_value=0))
def test_volume_moving_mean_branch_specific_behavior_warmup(values, warmup_min):
    result = volume_moving_mean(values, warmup_min=warmup_min)
    assert result is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), warmup_min=st.integers(min_value=1))
def test_volume_moving_mean_return_postcondition_none(values, warmup_min):
    result = volume_moving_mean(values, warmup_min=warmup_min)
    assert result is not None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), warmup_min=st.integers(min_value=1))
def test_volume_moving_mean_return_postcondition_mean(values, warmup_min):
    result = volume_moving_mean(values, warmup_min=warmup_min)
    assert isinstance(result, float)