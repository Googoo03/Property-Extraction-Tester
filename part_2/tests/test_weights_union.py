import hypothesis.strategies as st
from hypothesis import given
from dataset.python_programs.weights_union import weights_union

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = weights_union(left, right)
    assert len(output) == len(left) + len(right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        a, b = left[i], right[j]
        if a < b:
            merged.append(a)
            i += 1
        elif b < a:
            merged.append(b)
            j += 1
        else:
            merged.append(a)
            merged.append(b)
            i += 1
            j += 1
        assert merged == sorted(merged)
        assert set(merged) == set(left[:i] + right[:j])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_a_less_than_b(left, right):
    if left and right:
        a, b = left[0], right[0]
        if a < b:
            merged = weights_union(left, right)
            assert merged[0] == a
            assert merged[0] != b

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_b_less_than_a(left, right):
    if left and right:
        a, b = left[0], right[0]
        if b < a:
            merged = weights_union(left, right)
            assert merged[0] == b
            assert merged[0] != a

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_a_equals_b(left, right):
    if left and right:
        a, b = left[0], right[0]
        if a == b:
            merged = weights_union(left, right)
            assert merged[0] == a
            assert merged[1] == b

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_bug_fix(left, right):
    if left and right:
        merged = weights_union(left, right)
        if merged and left and right and merged[-1] == left[-1] == right[-1]:
            assert merged[-1] != left[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = weights_union(left, right)
    assert isinstance(output, list)
    assert all(isinstance(x, int) for x in output)