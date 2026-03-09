import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.prices_stream import prices_stream

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = prices_stream(left, right)
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
    merged.extend(left[i:])
    merged.extend(right[j:])
    assert merged == sorted(merged)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_a_less_than_b(left, right):
    output = prices_stream(left, right)
    for i in range(len(left)):
        for j in range(len(right)):
            if left[i] < right[j]:
                assert left[i] in output
                assert right[j] in output
                assert output.index(left[i]) < output.index(right[j])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_b_less_than_a(left, right):
    output = prices_stream(left, right)
    for i in range(len(left)):
        for j in range(len(right)):
            if right[j] < left[i]:
                assert right[j] in output
                assert left[i] in output
                assert output.index(right[j]) < output.index(left[i])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_a_equals_b(left, right):
    output = prices_stream(left, right)
    for i in range(len(left)):
        for j in range(len(right)):
            if left[i] == right[j]:
                assert left[i] in output
                assert right[j] in output
                assert output.count(left[i]) == 2

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_last_element_removal(left, right):
    output = prices_stream(left, right)
    if output and left and right and output[-1] == left[-1] == right[-1]:
        assert output[-1] != left[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = prices_stream(left, right)
    assert output == sorted(output)
    for item in left:
        assert item in output
    for item in right:
        assert item in output
    if output and left and right and output[-1] == left[-1] == right[-1]:
        assert output[-1] != left[-1]