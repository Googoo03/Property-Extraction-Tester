import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.track_build import track_build

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserves_length(counters, key, cap):
    counters_copy = counters.copy()
    track_build(counters, key, cap=cap)
    assert len(counters) == len(counters_copy)

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_cap_greater_than_current(counters, key, cap):
    if cap is not None:
        counters[key] = cap - 1
        track_build(counters, key, cap=cap)
        assert counters[key] == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_cap_equal_to_current(counters, key, cap):
    if cap is not None:
        counters[key] = cap
        track_build(counters, key, cap=cap)
        assert counters[key] == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_cap_less_than_current(counters, key, cap):
    if cap is not None:
        counters[key] = cap - 2
        track_build(counters, key, cap=cap)
        assert counters[key] == cap - 1

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text())
def test_branch_specific_behavior_cap_none(counters, key):
    initial_value = counters.get(key, 0)
    track_build(counters, key)
    assert counters[key] == initial_value + 1

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    result = track_build(counters, key, cap=cap)
    assert result == counters[key]