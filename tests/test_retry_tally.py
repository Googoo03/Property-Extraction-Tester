import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.retry_tally import retry_tally

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserve_length(counters, key, cap):
    original_length = len(counters)
    retry_tally(counters, key, cap=cap)
    assert len(counters) == original_length

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior(counters, key, cap):
    counters_copy = counters.copy()
    if cap is not None and counters_copy.get(key, 0) > cap:
        retry_tally(counters_copy, key, cap=cap)
        assert counters_copy[key] == cap
    else:
        retry_tally(counters_copy, key, cap=cap)
        assert counters_copy[key] == counters.get(key, 0) + 1

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    result = retry_tally(counters, key, cap=cap)
    assert result == counters[key]

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_key_presence(counters, key, cap):
    try:
        retry_tally(counters, key, cap=cap)
    except TypeError:
        pytest.fail("Key is not a valid hashable type for dictionary access")

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_counters_modification(counters, key, cap):
    original_value = counters.get(key, 0)
    retry_tally(counters, key, cap=cap)
    if cap is None or original_value < cap:
        assert counters[key] == original_value + 1
    else:
        assert counters[key] == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_non_negative_count(counters, key, cap):
    retry_tally(counters, key, cap=cap)
    assert counters[key] >= 0

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_no_clamping(counters, key, cap):
    if cap is None or counters.get(key, 0) <= cap:
        original_value = counters.get(key, 0)
        retry_tally(counters, key, cap=cap)
        assert counters[key] == original_value + 1

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_side_effect(counters, key, cap):
    original_counters = counters.copy()
    retry_tally(counters, key, cap=cap)
    assert counters is not original_counters
    assert counters == {**original_counters, key: counters.get(key, 0)}