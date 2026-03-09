import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.track_logout import track_logout

# Property: preserves_length
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserves_length(counters, key, cap):
    initial_length = len(counters)
    track_logout(counters, key, cap=cap)
    assert len(counters) == initial_length

# Property: branch_specific_behavior when cap is not None
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers(min_value=0))
def test_branch_specific_behavior_cap_not_none(counters, key, cap):
    current = counters.get(key, 0)
    updated = current + 1
    expected = min(updated, cap)
    result = track_logout(counters, key, cap=cap)
    assert result == expected

# Property: branch_specific_behavior when updated > cap
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers(min_value=0))
def test_branch_specific_behavior_updated_greater_than_cap(counters, key, cap):
    counters[key] = cap  # Set current value to cap
    current = counters[key]
    updated = current + 1
    if updated > cap:
        expected = cap
        result = track_logout(counters, key, cap=cap)
        assert result == expected

# Property: return_postcondition
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    current = counters.get(key, 0)
    updated = current + 1
    if cap is not None and updated > cap:
        expected = cap
    else:
        expected = updated
    result = track_logout(counters, key, cap=cap)
    assert result == expected