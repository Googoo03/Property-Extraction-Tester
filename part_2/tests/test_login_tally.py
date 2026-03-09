from hypothesis import given, strategies as st
from hypothesis.strategies import SearchStrategy
import pytest
from typing import Dict

# Assuming the function is in the correct path
from dataset.python_programs.login_tally import login_tally

# Define a strategy for the counters dictionary
def counters_strategy() -> SearchStrategy[Dict[str, int]]:
    return st.dictionaries(st.text(), st.integers())

# Test for 'preserves_length' property
@given(counters=counters_strategy(), key=st.text(), cap=st.integers())
def test_preserves_length(counters: Dict[str, int], key: str, cap: int):
    # The 'preserves_length' property as described doesn't make sense for this function
    # because it's about a dictionary, not a sequence. However, we can test that
    # the dictionary length either stays the same or increases by 1.
    initial_length = len(counters)
    login_tally(counters, key, cap=cap)
    final_length = len(counters)
    assert final_length == initial_length or final_length == initial_length + 1

# Test for branch when 'cap is not None'
@given(counters=counters_strategy(), key=st.text(), cap=st.integers(min_value=0))
def test_branch_cap_not_none(counters: Dict[str, int], key: str, cap: int):
    # Test behavior when cap is not None
    current = counters.get(key, 0)
    result = login_tally(counters, key, cap=cap)
    if current + 1 > cap:
        assert result == cap
    else:
        assert result == current + 1

# Test for branch when 'updated > cap'
@given(counters=counters_strategy(), key=st.text(), cap=st.integers(min_value=0))
def test_branch_updated_greater_than_cap(counters: Dict[str, int], key: str, cap: int):
    # This is essentially the same as the previous test but more specific
    current = counters.get(key, 0)
    result = login_tally(counters, key, cap=cap)
    if current >= cap:
        assert result == cap
    else:
        assert result == current + 1

# Test for return postcondition
@given(counters=counters_strategy(), key=st.text(), cap=st.integers())
def test_return_postcondition(counters: Dict[str, int], key: str, cap: int):
    current = counters.get(key, 0)
    result = login_tally(counters, key, cap=cap)
    if cap is not None and current >= cap:
        assert result == cap
    else:
        assert result == current + 1