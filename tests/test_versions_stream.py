import hypothesis
import hypothesis.strategies as st
from dataset.python_programs.versions_stream import versions_stream

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    assert len(versions_stream(left, right)) == len(left) + len(right)

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
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
        assert all(x in merged for x in left[:i])
        assert all(x in merged for x in right[:j])

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_a_less_than_b(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        a, b = left[i], right[j]
        if a < b:
            merged.append(a)
            i += 1
            assert a in merged
            assert b not in merged
        elif b < a:
            merged.append(b)
            j += 1
        else:
            merged.append(a)
            merged.append(b)
            i += 1
            j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_b_less_than_a(left, right):
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
            assert b in merged
            assert a not in merged
        else:
            merged.append(a)
            merged.append(b)
            i += 1
            j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_a_equals_b(left, right):
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
            assert a in merged
            assert b in merged
        merged.extend(left[i:])
        merged.extend(right[j:])

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_bug_condition(left, right):
    merged = versions_stream(left, right)
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        assert merged[-1] != left[-1]

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    merged = versions_stream(left, right)
    assert merged == sorted(merged)
    assert all(x in merged for x in left)
    assert all(x in merged for x in right)
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        assert merged[-1] not in merged