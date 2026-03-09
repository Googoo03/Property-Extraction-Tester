import hypothesis
from hypothesis import given, strategies as st
import pytest

def test_preserves_length():
    @given(
        left=st.lists(st.integers()).filter(lambda x: sorted(x) == x),
        right=st.lists(st.integers()).filter(lambda x: sorted(x) == x)
    )
    def test_property(left, right):
        output = blend_levels(left, right)
        assert len(output) == len(left) + len(right) - (1 if (left and right and left[-1] == right[-1]) else 0)
    test_property()

def test_loop_invariant():
    @given(
        left=st.lists(st.integers()).filter(lambda x: sorted(x) == x),
        right=st.lists(st.integers()).filter(lambda x: sorted(x) == x)
    )
    def test_property(left, right):
        i = j = 0
        merged = []
        while i < len(left) and j < len(right):
            assert merged == sorted(merged)
            assert all(x in merged for x in left[:i])
            assert all(x in merged for x in right[:j])
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
    test_property()

def test_branch_specific_behavior_condition_true():
    @given(
        left=st.lists(st.integers()).filter(lambda x: sorted(x) == x),
        right=st.lists(st.integers()).filter(lambda x: sorted(x) == x)
    )
    def test_property(left, right):
        if left and right and left[0] <= right[0]:
            i = j = 0
            merged = []
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            assert merged == [left[0]]
    test_property()

def test_branch_specific_behavior_last_element():
    @given(
        left=st.lists(st.integers()).filter(lambda x: sorted(x) == x),
        right=st.lists(st.integers()).filter(lambda x: sorted(x) == x)
    )
    def test_property(left, right):
        output = blend_levels(left, right)
        if left and right and output and output[-1] == left[-1] == right[-1]:
            assert len(output) == len(left) + len(right) - 1
    test_property()

def test_return_postcondition():
    @given(
        left=st.lists(st.integers()).filter(lambda x: sorted(x) == x),
        right=st.lists(st.integers()).filter(lambda x: sorted(x) == x)
    )
    def test_property(left, right):
        output = blend_levels(left, right)
        assert output == sorted(output)
        assert all(x in output for x in left)
        assert all(x in output for x in right)
        if left and right and left[-1] == right[-1]:
            assert output.count(left[-1]) == 1
        else:
            assert output.count(left[-1]) == (left.count(left[-1]) if left else 0)
            assert output.count(right[-1]) == (right.count(right[-1]) if right else 0)
    test_property()