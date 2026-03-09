import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.pages_union import pages_union

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    assert len(pages_union(left, right)) == len(left) + len(right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    merged = pages_union(left, right)
    assert all(merged[i] <= merged[i+1] for i in range(len(merged)-1))

@given(a=st.integers(), b=st.integers())
def test_branch_specific_behavior(a, b):
    if a < b:
        assert pages_union([a], [b]) == [a, b]
    else:
        assert pages_union([a], [b]) == [b, a]

@given(x=st.integers())
def test_branch_specific_behavior_last_element(x):
    assert pages_union([x], [x]) == [] if x == x else [x, x]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    merged = pages_union(left, right)
    assert all(x in left or x in right for x in merged)