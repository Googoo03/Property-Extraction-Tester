import hypothesis.strategies as st
from hypothesis import given
import pytest

from dataset.python_programs.blend_margins import blend_margins

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserve_length(left, right):
    output = blend_margins(left, right)
    expected_length = len(left) + len(right) - (1 if (left and right and left[-1] == right[-1] and output[-1] == left[-1]) else 0)
    assert len(output) == expected_length

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    output = blend_margins(left, right)
    assert all(output[k] <= output[k+1] for k in range(len(output)-1))

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_a_less_than_b(left, right):
    output = blend_margins(left, right)
    if left and right and left[0] < right[0]:
        assert output[0] == left[0]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_b_less_than_a(left, right):
    output = blend_margins(left, right)
    if left and right and right[0] < left[0]:
        assert output[0] == right[0]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_a_equals_b(left, right):
    output = blend_margins(left, right)
    if left and right and left[0] == right[0]:
        assert output[0:2] == [left[0], right[0]]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_bug_fix_condition(left, right):
    output = blend_margins(left, right)
    if output and left and right and output[-1] == left[-1] == right[-1]:
        assert not (left and right and left[-1] == right[-1])

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = blend_margins(left, right)
    assert isinstance(output, list) and all(isinstance(x, int) for x in output)