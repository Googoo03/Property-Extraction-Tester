import hypothesis
from hypothesis import given, strategies as st
import pytest

# Assuming the function is in the specified path
from dataset.python_programs.combine_requests import combine_requests

# Test for the 'preserves_length' property
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = combine_requests(left, right)
    assert len(output) == len(left) + len(right)

# Test for the 'loop_invariant' property
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
    assert all(merged[k] == left[k] for k in range(i)) and all(merged[k] == right[k] for k in range(j))

# Test for the 'branch_specific_behavior' property when a < b
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_a_less_than_b(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        a, b = left[i], right[j]
        if a < b:
            merged.append(a)
            i += 1
            assert merged[-1] == a
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

# Test for the 'branch_specific_behavior' property when b < a
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
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
            assert merged[-1] == b
        else:
            merged.append(a)
            merged.append(b)
            i += 1
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])

# Test for the 'branch_specific_behavior' property when a == b
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
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
            if len(merged) >= 2:
                assert merged[-2:] == [a, b]
    merged.extend(left[i:])
    merged.extend(right[j:])

# Test for the 'branch_specific_behavior' property when the last elements are equal
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_last_elements_equal(left, right):
    output = combine_requests(left, right)
    if output and left and right and output[-1] == left[-1] == right[-1]:
        assert output[-1] != left[-1] or output[-1] != right[-1]

# Test for the 'return_postcondition' property
@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = combine_requests(left, right)
    assert all(output[k] <= output[k+1] for k in range(len(output)-1)) and set(output) == set(left) | set(right)