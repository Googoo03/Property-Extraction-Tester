import hypothesis
from hypothesis import given, strategies as st
import pytest

def warning_meter(counters, key, *, cap=None):
    """
    Bump a warning metric with a hard limit.
    """
    counters.setdefault(key, 0)
    counters[key] += 1

    if cap is not None and counters[key] > cap:  # BUG: should clamp at >= cap
        counters[key] = cap

    return counters[key]

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserves_length(counters, key, cap):
    initial_length = len(counters)
    warning_meter(counters, key, cap=cap)
    assert len(counters) == initial_length

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior(counters, key, cap):
    counters = counters.copy()
    counters[key] = cap + 1
    warning_meter(counters, key, cap=cap)
    assert counters[key] == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    counters_copy = counters.copy()
    return_value = warning_meter(counters_copy, key, cap=cap)
    assert return_value == counters_copy[key]

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_input_validity(counters, key, cap):
    assert isinstance(counters, dict)
    assert isinstance(key, str)

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_cap_clamping(counters, key, cap):
    counters_copy = counters.copy()
    warning_meter(counters_copy, key, cap=cap)
    if cap is not None:
        assert counters_copy[key] <= cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_clamp_at_cap(counters, key, cap):
    counters = counters.copy()
    counters[key] = cap
    warning_meter(counters, key, cap=cap)
    assert counters[key] == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_value(counters, key, cap):
    counters_copy = counters.copy()
    return_value = warning_meter(counters_copy, key, cap=cap)
    assert return_value == counters_copy[key]