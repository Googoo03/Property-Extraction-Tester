import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.combine_offsets import combine_offsets

# Property: preserves_length
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = combine_offsets(left, right)
    assert len(output) == len(left) + len(right)

# Property: loop_invariant
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
    merged.extend(left[li:])
    merged.extend(right[ri:])
    expected = merged
    actual = combine_offsets(left, right)
    assert actual == expected

# Property: branch_specific_behavior (left[li] < right[ri])
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_left_less_than_right(left, right):
    if left and right:
        li = ri = 0
        while li < len(left) and ri < len(right):
            if left[li] < right[ri]:
                assert combine_offsets(left, right)[li + ri] == left[li]
                break
            ri += 1

# Property: branch_specific_behavior (merged and left and right and merged[-1] == left[-1] == right[-1])
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_duplicate_removal(left, right):
    if left and right and left[-1] == right[-1]:
        output = combine_offsets(left, right)
        if output and left and right and output[-1] == left[-1] == right[-1]:
            assert output[-1] != left[-1]

# Property: return_postcondition
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = combine_offsets(left, right)
    assert isinstance(output, list)
    assert all(isinstance(x, int) for x in output)