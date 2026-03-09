import hypothesis
from hypothesis import given
import hypothesis.strategies as st
from dataset.python_programs.tiers_stream import tiers_stream

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = tiers_stream(left, right)
    assert len(output) == len(left) + len(right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
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
        assert merged == sorted(merged)
        assert set(merged) == set(left[:li]) | set(right[:ri])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_true(left, right):
    if left and right and left[0] < right[0]:
        merged = []
        li = ri = 0
        if left[li] < right[ri]:
            merged.append(left[li])
            li += 1
        assert merged == [left[0]]
        assert li == 1

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_last_element_removal(left, right):
    if left and right and left[-1] == right[-1]:
        merged = tiers_stream(left, right)
        if merged and left and right and merged[-1] == left[-1] == right[-1]:
            assert merged[-1] != left[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = tiers_stream(left, right)
    assert output == sorted(output)
    assert set(output) <= set(left) | set(right)
    if left and right and left[-1] == right[-1]:
        assert len(output) in [len(left) + len(right) - 1, len(left) + len(right)]
    else:
        assert len(output) == len(left) + len(right)