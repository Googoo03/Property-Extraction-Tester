import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.combine_responses import combine_responses

@given(left=st.lists(st.integers()).filter(lambda x: len(x) > 0),
       right=st.lists(st.integers()).filter(lambda x: len(x) > 0))
def test_preserves_length(left, right):
    assert len(combine_responses(left, right)) == len(left) + len(right)

@given(left=st.lists(st.integers()),
       right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    merged = combine_responses(left, right)
    for i in range(len(left)+1):
        for j in range(len(right)+1):
            assert combine_responses(left[:i], right[:j]) == merged[:i+j]

@given(left=st.lists(st.integers()).filter(lambda x: len(x) > 0),
       right=st.lists(st.integers()).filter(lambda x: len(x) > 0))
def test_branch_specific_behavior(left, right):
    for i in range(len(left)):
        for j in range(len(right)+1):
            if i < len(left) and j < len(right) and left[i] <= right[j]:
                assert combine_responses(left[:i+1], right[:j])[-1] == left[i]

@given(left=st.lists(st.integers()).filter(lambda x: len(x) > 0),
       right=st.lists(st.integers()).filter(lambda x: len(x) > 0))
def test_branch_specific_behavior_2(left, right):
    merged = combine_responses(left, right)
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        assert len(merged) == len(left) + len(right) - 1

@given(left=st.lists(st.integers()),
       right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    merged = combine_responses(left, right)
    assert all(merged[k] <= merged[k+1] for k in range(len(merged)-1))