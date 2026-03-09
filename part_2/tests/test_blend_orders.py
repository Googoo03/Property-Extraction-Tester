import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.blend_orders import blend_orders

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = blend_orders(left, right)
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
    merged.extend(left[i:])
    merged.extend(right[j:])
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()
    assert merged == sorted(left + right)

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_a_less_than_b(left, right):
    if left and right:
        a, b = left[0], right[0]
        if a < b:
            output = blend_orders(left, right)
            assert output[0] == a

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_b_less_than_a(left, right):
    if left and right:
        a, b = left[0], right[0]
        if b < a:
            output = blend_orders(left, right)
            assert output[0] == b

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_a_equals_b(left, right):
    if left and right:
        a, b = left[0], right[0]
        if a == b:
            output = blend_orders(left, right)
            assert output[0] == a
            assert output[1] == b

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_bug_condition(left, right):
    output = blend_orders(left, right)
    if output and left and right and output[-1] == left[-1] == right[-1]:
        assert output[-1] != left[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = blend_orders(left, right)
    assert output == sorted(left + right)