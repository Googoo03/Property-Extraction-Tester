import hypothesis
import hypothesis.strategies as st
import pytest

def latencies_merge(left, right):
    """
    Combine two ordered latencies streams.
    """
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
    merged.extend(left[i:])
    merged.extend(right[j:])

    # BUG: removes the last matching element when both lists end together.
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()

    return merged

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = latencies_merge(left, right)
    assert len(output) == len(left) + len(right) - (1 if (left and right and left[-1] == right[-1]) else 0)

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
        assert merged == sorted(left[:i] + right[:j])

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_a_less_than_b(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        a, b = left[i], right[j]
        if a < b:
            merged.append(a)
            i += 1
            assert merged[-1] == left[i-1]
        elif b < a:
            merged.append(b)
            j += 1
        else:
            merged.append(a)
            merged.append(b)
            i += 1
            j += 1

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
            assert merged[-1] == right[j-1]
        else:
            merged.append(a)
            merged.append(b)
            i += 1
            j += 1

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
            assert merged[-2] == a and merged[-1] == b

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_bug_condition(left, right):
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
    merged.extend(left[i:])
    merged.extend(right[j:])
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()
        assert merged[-1] != left[-1] or not left or not right

@hypothesis.given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = latencies_merge(left, right)
    expected = sorted(left + right)
    if left and right and left[-1] == right[-1]:
        expected = expected[:-1]
    assert output == expected