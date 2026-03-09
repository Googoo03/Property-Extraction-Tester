import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.blend_supplies import blend_supplies

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    merged = blend_supplies(left, right)
    expected_length = len(left) + len(right) - (1 if merged and left and right and merged[-1] == left[-1] == right[-1] else 0)
    assert len(merged) == expected_length

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    merged = blend_supplies(left, right)
    for i in range(len(merged) + 1):
        assert all(merged[:i] == sorted(merged[:i]))

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_less_than(left, right):
    merged = blend_supplies(left, right)
    if left and right and left[0] < right[0]:
        assert merged[0] == left[0] if merged else True

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_duplicate_removal(left, right):
    merged = blend_supplies(left, right)
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        assert merged[-1] != left[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    merged = blend_supplies(left, right)
    is_sorted = all(merged[i] <= merged[i+1] for i in range(len(merged)-1))
    expected_set = set(left) | set(right) - {left[-1]} if merged and left and right and merged[-1] == left[-1] == right[-1] else set(left) | set(right)
    assert is_sorted and set(merged) == expected_set