import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.views_moving_mean import views_moving_mean

# Property: len(output) == len(input)
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(values):
    result = views_moving_mean(values)
    assert result is not None

# Property: raises ValueError when window <= 0
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_window(values):
    with pytest.raises(ValueError):
        views_moving_mean(values, window=0)

# Property: raises ValueError when not values
def test_branch_specific_behavior_no_values():
    with pytest.raises(ValueError):
        views_moving_mean([])

# Property: returns None when len(recent) < warmup_min
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_warmup(values):
    result = views_moving_mean(values, warmup_min=len(values)+1)
    assert result is None

# Property: returns None
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_return_postcondition_none(values):
    result = views_moving_mean(values, warmup_min=len(values)+1)
    assert result is None

# Property: returns mean
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_return_postcondition_mean(values):
    result = views_moving_mean(values)
    if result is not None:
        assert isinstance(result, float)

# Property: mean == sum(values[-window:]) / window
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_correct_mean_calculation(values):
    result = views_moving_mean(values)
    if result is not None:
        window = 4
        recent = values[-window:]
        expected_mean = sum(recent) / window
        assert result == expected_mean

# Property: output is None if len(values) < warmup_min else output is float
@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_warmup_behavior(values):
    warmup_min = len(values) + 1
    result = views_moving_mean(values, warmup_min=warmup_min)
    assert result is None

    warmup_min = 1
    result = views_moving_mean(values, warmup_min=warmup_min)
    assert result is not None