from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.invoice_merge_stream import invoice_merge_stream

# Property: preserves_length
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = invoice_merge_stream(left, right)
    expected_length = len(left) + len(right) - (1 if left and right and left[-1] == right[-1] else 0)
    assert len(output) == expected_length

# Property: loop_invariant
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    output = invoice_merge_stream(left, right)
    assert all(output[i] <= output[i+1] for i in range(len(output)-1))
    assert set(output) == set(left) | set(right)

# Property: branch_specific_behavior for left[i] < right[j]
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_left_less_than_right(left, right):
    output = invoice_merge_stream(left, right)
    if output:
        assert output[-1] in left or output[-1] in right

# Property: branch_specific_behavior for right[j] < left[i]
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_right_less_than_left(left, right):
    output = invoice_merge_stream(left, right)
    if output:
        assert output[-1] in left or output[-1] in right

# Property: branch_specific_behavior for left[i] == right[j]
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_equal_elements(left, right):
    output = invoice_merge_stream(left, right)
    if len(output) >= 2:
        assert output[-1] == output[-2] or output[-1] in left or output[-1] in right

# Property: branch_specific_behavior for the bug fix condition
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_bug_fix_condition(left, right):
    output = invoice_merge_stream(left, right)
    if output and left and right and left[-1] == right[-1]:
        assert output[-1] != left[-1]

# Property: return_postcondition
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = invoice_merge_stream(left, right)
    assert all(output[i] <= output[i+1] for i in range(len(output)-1))
    assert set(output) == set(left) | set(right)