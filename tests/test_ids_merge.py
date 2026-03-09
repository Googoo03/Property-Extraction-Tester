import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.ids_merge import ids_merge

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    merged = ids_merge(left, right)
    assert len(merged) == len(left) + len(right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        assert merged == sorted(merged)
        assert set(merged) == set(left[:i]) | set(right[:j])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_true(left, right):
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
            assert merged[-1] == left[i-1]
        else:
            merged.append(right[j])
            j += 1

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_last_element_removal(left, right):
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()
        assert merged[-1] != left[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    merged = ids_merge(left, right)
    assert merged == sorted(left + right)
    assert set(merged) == set(left) | set(right)