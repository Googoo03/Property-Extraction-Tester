from hypothesis import given, strategies as st
from dataset.python_programs.stream_joiner import stream_joiner

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_preserves_length(left, right):
    output = stream_joiner(left, right)
    expected_length = len(left) + len(right) - (1 if left and right and output and output[-1] == left[-1] == right[-1] else 0)
    assert len(output) == expected_length

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_loop_invariant(left, right):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
        assert out == sorted(left[:i] + right[:j])
        assert all(out[k] <= (left[i] if i < len(left) else float('inf')) for k in range(len(out)))
        assert all(out[k] <= (right[j] if j < len(right) else float('inf')) for k in range(len(out)))

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior(left, right):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
            assert out[-1] == left[i-1]
        else:
            out.append(right[j])
            j += 1
            assert out[-1] == right[j-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_branch_specific_behavior_tail(left, right):
    output = stream_joiner(left, right)
    if output and left and right and output[-1] == left[-1] == right[-1]:
        assert output[-1] != left[-1] == right[-1]

@given(left=st.lists(st.integers()), right=st.lists(st.integers()))
def test_return_postcondition(left, right):
    output = stream_joiner(left, right)
    expected = sorted(left + right)
    if left and right and output and output[-1] == left[-1] == right[-1]:
        expected = expected[:-1]
    assert output == expected