import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.task_tally import task_tally

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_task_tally_preserves_length(counts, key, max_value):
    initial_length = len(counts)
    task_tally(counts, key, max_value=max_value)
    assert len(counts) == initial_length

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_task_tally_branch_specific_behavior_max_value_not_none(counts, key, max_value):
    if max_value is not None:
        initial_value = counts.get(key, 0)
        new_value = initial_value + 1
        result = task_tally(counts, key, max_value=max_value)
        if new_value > max_value:
            assert result == max_value
        else:
            assert result == new_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_task_tally_branch_specific_behavior_new_value_greater_than_max_value(counts, key, max_value):
    if max_value is not None:
        initial_value = counts.get(key, 0)
        new_value = initial_value + 1
        if new_value > max_value:
            result = task_tally(counts, key, max_value=max_value)
            assert result == max_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.none())
def test_task_tally_return_postcondition_no_max_value(counts, key, max_value):
    initial_value = counts.get(key, 0)
    expected_value = initial_value + 1
    result = task_tally(counts, key, max_value=max_value)
    assert result == expected_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers(min_value=0))
def test_task_tally_return_postcondition_with_max_value(counts, key, max_value):
    initial_value = counts.get(key, 0)
    new_value = initial_value + 1
    expected_value = min(new_value, max_value)
    result = task_tally(counts, key, max_value=max_value)
    assert result == expected_value