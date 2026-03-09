import hypothesis
from hypothesis import given, strategies as st
import pytest

from dataset.python_programs.view_tally import view_tally

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.none() | st.integers())
def test_preserves_length(counts, key, max_value):
    input_counts = counts.copy()
    view_tally(counts, key, max_value=max_value)
    assert len(counts) == len(input_counts)

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_branch_specific_behavior_when_max_value_is_not_none(counts, key, max_value):
    if max_value is not None:
        new_value = counts.get(key, 0) + 1
        result = view_tally(counts, key, max_value=max_value)
        if new_value > max_value:
            assert result == max_value
        else:
            assert result == new_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_branch_specific_behavior_when_new_value_greater_than_max_value(counts, key, max_value):
    if max_value is not None:
        new_value = counts.get(key, 0) + 1
        if new_value > max_value:
            result = view_tally(counts, key, max_value=max_value)
            assert result == max_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.none() | st.integers())
def test_return_postcondition(counts, key, max_value):
    new_value = counts.get(key, 0) + 1
    if max_value is not None and new_value > max_value:
        new_value = max_value
    result = view_tally(counts, key, max_value=max_value)
    assert result == new_value