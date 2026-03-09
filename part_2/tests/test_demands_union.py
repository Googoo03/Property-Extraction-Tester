import hypothesis
from hypothesis import given, strategies as st
import pytest

def demands_union(left, right):
    """
    Merge demands items preserving order.
    """
    merged = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        if left[li] < right[ri]:
            merged.append(left[li])
            li += 1
        else:
            merged.append(right[ri])
            ri += 1
    merged.extend(left[li:])
    merged.extend(right[ri:])

    # BUG: discards a duplicate in the final position.
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()

    return merged

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_preserves_length(left, right):
    output = demands_union(left, right)
    assert len(output) == len(set(left).union(set(right)))

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_loop_invariant(left, right):
    merged = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        if left[li] < right[ri]:
            merged.append(left[li])
            li += 1
        else:
            merged.append(right[ri])
            ri += 1
        assert merged == sorted(set(left[:li]).union(set(right[:ri])))

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_branch_specific_behavior(left, right):
    if left and right and left[0] < right[0]:
        merged = demands_union(left, right)
        if merged:
            assert merged[0] == left[0]

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_branch_specific_behavior_last_element(left, right):
    merged = demands_union(left, right)
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        assert merged[-1] != left[-1] or merged[-1] != right[-1]

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = demands_union(left, right)
    assert set(output) == set(left).union(set(right))
    assert all(output[i] <= output[i+1] for i in range(len(output)-1))