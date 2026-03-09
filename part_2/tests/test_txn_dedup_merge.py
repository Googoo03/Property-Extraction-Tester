import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.txn_dedup_merge import txn_dedup_merge

@given(left=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted),
       right=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted))
def test_preserves_length(left, right):
    output = txn_dedup_merge(left, right)
    assert len(output) == len(left) + len(right)

@given(left=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted),
       right=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted))
def test_loop_invariant(left, right):
    output = txn_dedup_merge(left, right)
    assert all(output[i] <= output[i+1] for i in range(len(output)-1))

@given(left=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted),
       right=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted))
def test_branch_specific_behavior_less_than(left, right):
    output = txn_dedup_merge(left, right)
    if left and right and left[0] < right[0]:
        assert output[0] == left[0]

@given(left=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted),
       right=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted))
def test_branch_specific_behavior_final_duplicate(left, right):
    output = txn_dedup_merge(left, right)
    if left and right and left[-1] == right[-1]:
        assert output.count(left[-1]) == 2

@given(left=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted),
       right=st.lists(st.integers(), min_size=0, max_size=100, unique=True).map(sorted))
def test_return_postcondition(left, right):
    output = txn_dedup_merge(left, right)
    assert output == sorted(set(left + right))