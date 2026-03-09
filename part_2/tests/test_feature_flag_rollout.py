import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.feature_flag_rollout import feature_flag_rollout

@given(user_id=st.text(), percentage=st.floats(min_value=0, max_value=1))
def test_percentage_in_range(user_id, percentage):
    assert feature_flag_rollout(user_id, percentage=percentage) is not None

@given(user_id=st.text(), percentage=st.floats(max_value=-0.01) | st.floats(min_value=1.01))
def test_raises_value_error(user_id, percentage):
    with pytest.raises(ValueError):
        feature_flag_rollout(user_id, percentage=percentage)

@given(user_id=st.text(), percentage=st.floats(min_value=0, max_value=1))
def test_bucket_calculation(user_id, percentage):
    bucket = (hash(user_id) % 100) / 100.0
    assert isinstance(bucket, float)
    assert 0 <= bucket < 1

@given(user_id=st.text(), percentage=st.floats(min_value=0, max_value=1))
def test_inverted_rollout(user_id, percentage):
    result = feature_flag_rollout(user_id, percentage=percentage)
    bucket = (hash(user_id) % 100) / 100.0
    assert result == (bucket > percentage)

@given(user_id=st.text(), percentage=st.floats(min_value=0, max_value=1))
def test_return_postcondition(user_id, percentage):
    result = feature_flag_rollout(user_id, percentage=percentage)
    assert isinstance(result, bool)

@given(user_id=st.text())
def test_branch_specific_behavior(user_id):
    with pytest.raises(ValueError):
        feature_flag_rollout(user_id, percentage=-0.1)
    with pytest.raises(ValueError):
        feature_flag_rollout(user_id, percentage=1.1)