import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.histogram_bucket_merge import histogram_bucket_merge

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = histogram_bucket_merge(left, right)
    assert len(output) == len(left) + len(right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    i = j = 0
    merged = []
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] < right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        elif right_sorted[j] < left_sorted[i]:
            merged.append(right_sorted[j])
            j += 1
        else:
            merged.append(left_sorted[i])
            merged.append(right_sorted[j])
            i += 1
            j += 1
    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])
    assert all(merged[k] <= merged[k+1] for k in range(len(merged)-1))
    assert merged == sorted(left_sorted[:i] + right_sorted[:j])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_less_than(left, right):
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    i = j = 0
    merged = []
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] < right_sorted[j]:
            merged.append(left_sorted[i])
            if merged:
                assert merged[-1] == left_sorted[i]
            i += 1
        elif right_sorted[j] < left_sorted[i]:
            merged.append(right_sorted[j])
            j += 1
        else:
            merged.append(left_sorted[i])
            merged.append(right_sorted[j])
            i += 1
            j += 1
    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_greater_than(left, right):
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    i = j = 0
    merged = []
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] < right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        elif right_sorted[j] < left_sorted[i]:
            merged.append(right_sorted[j])
            if merged:
                assert merged[-1] == right_sorted[j]
            j += 1
        else:
            merged.append(left_sorted[i])
            merged.append(right_sorted[j])
            i += 1
            j += 1
    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_equal(left, right):
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    i = j = 0
    merged = []
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] < right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        elif right_sorted[j] < left_sorted[i]:
            merged.append(right_sorted[j])
            j += 1
        else:
            merged.append(left_sorted[i])
            merged.append(right_sorted[j])
            if len(merged) >= 2:
                assert merged[-2:] == [left_sorted[i], right_sorted[j]]
            i += 1
            j += 1
    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_last_duplicate(left, right):
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    i = j = 0
    merged = []
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] < right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        elif right_sorted[j] < left_sorted[i]:
            merged.append(right_sorted[j])
            j += 1
        else:
            merged.append(left_sorted[i])
            merged.append(right_sorted[j])
            i += 1
            j += 1
    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])
    if merged and left_sorted and right_sorted and merged[-1] == left_sorted[-1] == right_sorted[-1]:
        assert merged[-1] != left_sorted[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = histogram_bucket_merge(left, right)
    assert sorted(output) == sorted(left + right)