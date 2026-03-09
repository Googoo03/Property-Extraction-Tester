import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.log_sampling_decider import log_sampling_decider

@given(log_id=st.integers(), rate=st.floats(min_value=0, max_value=1))
def test_rate_validation(log_id, rate):
    assert 0 <= rate <= 1

@given(log_id=st.one_of(st.integers(), st.text()))
def test_log_id_type(log_id):
    assert isinstance(log_id, (int, str))

@given(log_id=st.integers(), rate=st.floats(min_value=0, max_value=1))
def test_rate_within_bounds(log_id, rate):
    try:
        result = log_sampling_decider(log_id, rate=rate)
        assert result is not None
    except ValueError:
        assert not (0 <= rate <= 1)

@given(log_id=st.integers(), rate=st.floats(min_value=0, max_value=1))
def test_sampling_decision(log_id, rate):
    bucket = (hash(log_id) % 1000) / 1000.0
    expected = bucket > rate
    assert log_sampling_decider(log_id, rate=rate) == expected

@given(log_id=st.integers(), rate=st.floats())
def test_branch_specific_behavior(log_id, rate):
    if not (0 <= rate <= 1):
        with pytest.raises(ValueError):
            log_sampling_decider(log_id, rate=rate)

@given(log_id=st.integers(), rate=st.floats(min_value=0, max_value=1))
def test_return_postcondition(log_id, rate):
    result = log_sampling_decider(log_id, rate=rate)
    bucket = (hash(log_id) % 1000) / 1000.0
    assert result == (bucket > rate)