import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.bump_refund import bump_refund

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_bump_refund_preserves_length(counts, key, max_value):
    # Since counts is a dictionary, we check if the length of the dictionary remains the same
    # after the function call. This property is not directly applicable to dictionaries.
    # Instead, we check if the key exists in the dictionary after the function call.
    initial_length = len(counts)
    bump_refund(counts, key, max_value=max_value)
    final_length = len(counts)
    assert initial_length == final_length

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_bump_refund_branch_specific_behavior_max_value_not_none(counts, key, max_value):
    if max_value is not None:
        new_value = counts.get(key, 0) + 1
        if new_value > max_value:
            new_value = max_value
        assert bump_refund(counts, key, max_value=max_value) == new_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_bump_refund_branch_specific_behavior_new_value_greater_than_max_value(counts, key, max_value):
    if max_value is not None:
        new_value = counts.get(key, 0) + 1
        if new_value > max_value:
            result = bump_refund(counts, key, max_value=max_value)
            assert result == max_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_bump_refund_return_postcondition(counts, key, max_value):
    initial_value = counts.get(key, 0)
    new_value = initial_value + 1
    if max_value is not None and new_value > max_value:
        new_value = max_value
    assert bump_refund(counts, key, max_value=max_value) == new_value