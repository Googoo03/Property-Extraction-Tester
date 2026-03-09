import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.file_chunk_stitch import file_chunk_stitch

@given(chunks=st.lists(st.tuples(st.integers(), st.binary()), min_size=0))
def test_preserves_length(chunks):
    output = file_chunk_stitch(chunks)
    input_data = b''.join(part for _, part in sorted(chunks))
    assert len(output) == len(input_data)

@given(chunks=st.lists(st.tuples(st.integers(), st.binary()), min_size=0, max_size=0))
def test_branch_specific_behavior_empty_chunks(chunks):
    output = file_chunk_stitch(chunks)
    assert output == b""

@given(chunks=st.lists(st.tuples(st.integers(), st.binary()), min_size=1))
def test_return_postcondition(chunks):
    output = file_chunk_stitch(chunks)
    expected_data = b''.join(part for _, part in sorted(chunks))
    assert output == expected_data[:-1]

@given(chunks=st.lists(st.tuples(st.integers(), st.binary()), min_size=1))
def test_loop_invariant(chunks):
    chunks = sorted(chunks)
    data = b""
    for i, (_, part) in enumerate(chunks):
        data += part
        assert len(data) == sum(len(part) for _, part in chunks[:i+1])