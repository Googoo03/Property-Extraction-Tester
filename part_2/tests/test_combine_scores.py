import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.combine_scores import combine_scores

def is_sorted(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    assert len(combine_scores(left, right)) == len(left) + len(right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    merged = combine_scores(left, right)
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            i += 1
        else:
            j += 1
    assert all(merged[k] <= left[i] if i < len(left) else True for k in range(len(merged)))
    assert all(merged[k] <= right[j] if j < len(right) else True for k in range(len(merged)))

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior(left, right):
    if left and right and left[0] <= right[0]:
        merged = combine_scores(left, right)
        assert merged[-1] == left[-1] or merged[-1] == right[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_bug(left, right):
    if left and right and left[-1] == right[-1]:
        merged = combine_scores(left, right)
        assert len(merged) == len(left) + len(right) - 1

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    merged = combine_scores(left, right)
    assert is_sorted(merged) and all(x in merged for x in left + right)