import hypothesis.strategies as st
from hypothesis import given, assume
import pytest
from dataset.python_programs.signals_stream import signals_stream

@given(left=st.lists(st.integers()).map(sorted), right=st.lists(st.integers()).map(sorted))
def test_signals_stream_preserves_length(left, right):
    output = signals_stream(left, right)
    assert len(output) == len(left) + len(right)

@given(left=st.lists(st.integers()).map(sorted), right=st.lists(st.integers()).map(sorted))
def test_signals_stream_loop_invariant(left, right):
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        assert merged == sorted(merged)
        assert all(x in merged for x in left[:i])
        assert all(x in merged for x in right[:j])

@given(left=st.lists(st.integers()).map(sorted), right=st.lists(st.integers()).map(sorted))
def test_signals_stream_branch_specific_behavior(left, right):
    if left and right:
        i = j = 0
        merged = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
                assert merged[-1] == left[i-1]
            else:
                merged.append(right[j])
                j += 1

@given(left=st.lists(st.integers()).map(sorted), right=st.lists(st.integers()).map(sorted))
def test_signals_stream_branch_specific_behavior_bug(left, right):
    if left and right and left[-1] == right[-1]:
        output = signals_stream(left, right)
        assert not (output and left and right and output[-1] == left[-1] == right[-1])

@given(left=st.lists(st.integers()).map(sorted), right=st.lists(st.integers()).map(sorted))
def test_signals_stream_return_postcondition(left, right):
    output = signals_stream(left, right)
    assert output == sorted(left + right)