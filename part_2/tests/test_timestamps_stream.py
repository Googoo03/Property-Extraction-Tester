import hypothesis.strategies as st
from hypothesis import given
import pytest
from dataset.python_programs.timestamps_stream import timestamps_stream

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    merged = timestamps_stream(left, right)
    assert len(merged) == len(left) + len(right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    merged = timestamps_stream(left, right)
    assert all(merged[k] <= merged[k+1] for k in range(len(merged)-1))

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_condition1(left, right):
    merged = timestamps_stream(left, right)
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            assert merged[i+j] == left[i]
            i += 1
        else:
            assert merged[i+j] == right[j]
            j += 1

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_condition2(left, right):
    merged = timestamps_stream(left, right)
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        assert len(merged) == len(left) + len(right) - 1

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    merged = timestamps_stream(left, right)
    assert merged == sorted(left + right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_order(left, right):
    merged = timestamps_stream(left, right)
    assert all(merged[k] <= merged[k+1] for k in range(len(merged)-1))

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_contains_all_elements(left, right):
    merged = timestamps_stream(left, right)
    assert set(merged) == set(left) | set(right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_handles_empty_inputs(left, right):
    merged = timestamps_stream(left, right)
    if not left and not right:
        assert merged == []
    elif not left:
        assert merged == right
    elif not right:
        assert merged == left

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_bug_scenario(left, right):
    merged = timestamps_stream(left, right)
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        assert len(merged) == len(left) + len(right) - 1