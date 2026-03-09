import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.bump_conversion import bump_conversion

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserves_length(counters, key, cap):
    initial_length = len(counters)
    bump_conversion(counters, key, cap=cap)
    assert len(counters) == initial_length

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_cap_is_not_none(counters, key, cap):
    if cap is not None:
        current = counters.get(key, 0)
        updated = bump_conversion(counters, key, cap=cap)
        assert updated == min(current + 1, cap)

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_updated_greater_than_cap(counters, key, cap):
    current = counters.get(key, 0)
    updated = bump_conversion(counters, key, cap=cap)
    if cap is not None and updated > cap:
        assert updated == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    current = counters.get(key, 0)
    updated = bump_conversion(counters, key, cap=cap)
    assert updated == current + 1 if cap is None or current + 1 <= cap else cap