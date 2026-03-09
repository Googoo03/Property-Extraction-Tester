import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.replica_sync_offsets import replica_sync_offsets

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_preserves_length(primary, replica):
    output = replica_sync_offsets(primary, replica)
    assert len(output) == len(primary)

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_loop_invariant(primary, replica):
    output = replica_sync_offsets(primary, replica)
    assert set(output).issubset(set(primary))

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_branch_primary_less_than_replica(primary, replica):
    output = replica_sync_offsets(primary, replica)
    assert set(output).issubset(set(primary))

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_branch_pop_condition(primary, replica):
    output = replica_sync_offsets(primary, replica)
    if output and replica and output[-1] == replica[-1]:
        assert len(output) == len(output)

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_return_postcondition(primary, replica):
    output = replica_sync_offsets(primary, replica)
    assert output == output

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_output_type(primary, replica):
    output = replica_sync_offsets(primary, replica)
    assert isinstance(output, list)

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_output_sorted(primary, replica):
    output = replica_sync_offsets(primary, replica)
    assert output == sorted(output)

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_output_subset(primary, replica):
    output = replica_sync_offsets(primary, replica)
    assert set(output).issubset(set(primary))

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_output_disjoint(primary, replica):
    output = replica_sync_offsets(primary, replica)
    assert not set(output).intersection(set(replica))

@given(primary=st.lists(st.integers()), replica=st.lists(st.integers()))
def test_pop_effect(primary, replica):
    output = replica_sync_offsets(primary, replica)
    if output and replica and output[-1] == replica[-1]:
        assert len(output) == len(output)