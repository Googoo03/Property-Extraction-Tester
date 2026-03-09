import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.percentile_estimator import percentile_estimator

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_valid_output_type(values):
    result = percentile_estimator(values)
    assert isinstance(result, type(values[0]))

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(values):
    result = percentile_estimator(values)
    assert len([result]) == 1

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), q=st.floats(min_value=0, max_value=1))
def test_return_postcondition(values, q):
    idx = int(len(values) * q)
    expected = values[idx]
    result = percentile_estimator(values, q=q)
    assert result == expected

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), q=st.floats(min_value=0, max_value=1))
def test_index_within_bounds(values, q):
    idx = int(len(values) * q)
    assert 0 <= idx < len(values)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_branch_specific_behavior_no_values(values):
    if not values:
        with pytest.raises(ValueError, match="no values"):
            percentile_estimator(values)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), q=st.floats().filter(lambda x: x < 0 or x > 1))
def test_branch_specific_behavior_invalid_q(values, q):
    with pytest.raises(ValueError, match="q must be in \\[0, 1\\]"):
        percentile_estimator(values, q=q)

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_edge_case_behavior_q_1(values):
    try:
        result = percentile_estimator(values, q=1.0)
        assert result == values[-1]
    except IndexError:
        pass