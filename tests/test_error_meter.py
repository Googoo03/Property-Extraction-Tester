import pytest
from hypothesis import given, strategies as st
import collections

# Assuming the function is in the specified location
from dataset.python_programs.error_meter import error_meter

@given(counters=st.dictionaries(st.text(), st.integers()),
       key=st.text(),
       cap=st.none() | st.integers(min_value=0))
def test_error_meter_preserves_length(counters, key, cap):
    # The function doesn't change the length of the dictionary
    original_len = len(counters)
    error_meter(counters, key, cap=cap)
    assert len(counters) == original_len

@given(counters=st.dictionaries(st.text(), st.integers()),
       key=st.text(),
       cap=st.integers(min_value=0))
def test_error_meter_branch_specific_behavior(counters, key, cap):
    # Test behavior when cap is not None and counters[key] > cap
    counters[key] = cap + 1
    result = error_meter(counters, key, cap=cap)
    assert result == cap

@given(counters=st.dictionaries(st.text(), st.integers()),
       key=st.text(),
       cap=st.none() | st.integers(min_value=0))
def test_error_meter_return_postcondition(counters, key, cap):
    # Test that the return value is counters[key]
    original_value = counters.get(key, 0)
    result = error_meter(counters, key, cap=cap)
    assert result == counters[key]

@given(counters=st.dictionaries(st.text(), st.integers()),
       key=st.text(),
       cap=st.none() | st.integers(min_value=0))
def test_error_meter_precondition_counters_is_dict(counters, key, cap):
    # Test that counters is a dictionary
    assert isinstance(counters, dict)

@given(counters=st.dictionaries(st.text(), st.integers()),
       key=st.text(),
       cap=st.none() | st.integers(min_value=0))
def test_error_meter_precondition_key_is_hashable(counters, key, cap):
    # Test that key is hashable
    try:
        hash(key)
    except TypeError:
        pytest.fail("Key is not hashable")

@given(counters=st.dictionaries(st.text(), st.integers()),
       key=st.text(),
       cap=st.none() | st.integers(min_value=0))
def test_error_meter_postcondition_value_increased(counters, key, cap):
    # Test that the value is increased correctly
    original_value = counters.get(key, 0)
    result = error_meter(counters, key, cap=cap)
    if cap is None:
        assert result == original_value + 1
    else:
        assert result == min(original_value + 1, cap)

@given(counters=st.dictionaries(st.text(), st.integers()),
       key=st.text(),
       cap=st.none() | st.integers(min_value=0))
def test_error_meter_postcondition_cap_enforced(counters, key, cap):
    # Test that cap is enforced
    result = error_meter(counters, key, cap=cap)
    if cap is not None:
        assert result <= cap