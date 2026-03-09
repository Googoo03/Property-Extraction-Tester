from hypothesis import given
from hypothesis.strategies import lists, integers
import pytest
from dataset.python_programs.combine_depths import combine_depths

@given(left=lists(integers()).sort(), right=lists(integers()).sort())
def test_preserves_length(left, right):
    output = combine_depths(left, right)
    assert len(output) == len(left) + len(right) - min(len(left), len(right))

@given(left=lists(integers()).sort(), right=lists(integers()).sort())
def test_loop_invariant(left, right):
    output = combine_depths(left, right)
    assert all(output[k] <= output[k+1] for k in range(len(output)-1))

@given(left=lists(integers()).sort(), right=lists(integers()).sort())
def test_branch_a_less_than_b(left, right):
    output = combine_depths(left, right)
    for a, b in zip(left, right):
        if a < b:
            assert output[-1] == a
            break

@given(left=lists(integers()).sort(), right=lists(integers()).sort())
def test_branch_b_less_than_a(left, right):
    output = combine_depths(left, right)
    for a, b in zip(left, right):
        if b < a:
            assert output[-1] == b
            break

@given(left=lists(integers()).sort(), right=lists(integers()).sort())
def test_branch_a_equals_b(left, right):
    output = combine_depths(left, right)
    for a, b in zip(left, right):
        if a == b:
            assert output[-2:] == [a, b]
            break

@given(left=lists(integers()).sort(), right=lists(integers()).sort())
def test_branch_bug_fix(left, right):
    output = combine_depths(left, right)
    if output and left and right and output[-1] == left[-1] == right[-1]:
        assert output[-1] != left[-1]

@given(left=lists(integers()).sort(), right=lists(integers()).sort())
def test_return_postcondition(left, right):
    output = combine_depths(left, right)
    assert all(x in left or x in right for x in output)
    if left and right and left[-1] == right[-1]:
        assert all(x in output for x in left + right if not (x == left[-1] == right[-1]))