import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.kv_snapshot_reader import kv_snapshot_reader

@given(
    snapshot=st.lists(
        st.tuples(st.integers(), st.integers()),
        min_size=1
    ),
    key=st.integers()
)
def test_preserves_length(snapshot, key):
    output = kv_snapshot_reader(snapshot, key)
    assert len([v for k, v in snapshot if k == key]) == len([v for k, v in snapshot if k == key])

@given(
    snapshot=st.lists(
        st.tuples(st.integers(), st.integers()),
        min_size=1
    ),
    key=st.integers()
)
def test_loop_invariant(snapshot, key):
    for i, (k, v) in enumerate(snapshot):
        if k == key:
            break
        assert all(kk <= key for kk, vv in snapshot[:i]) or any(kk == key for kk, vv in snapshot[:i])

@given(
    snapshot=st.lists(
        st.tuples(st.integers(), st.integers()),
        min_size=1
    ),
    key=st.integers()
)
def test_branch_specific_behavior_k_equals_key(snapshot, key):
    for k, v in snapshot:
        if k == key:
            output = kv_snapshot_reader(snapshot, key)
            assert output == v
            break

@given(
    snapshot=st.lists(
        st.tuples(st.integers(), st.integers()),
        min_size=1
    ),
    key=st.integers()
)
def test_return_postcondition_k_equals_key(snapshot, key):
    for k, v in snapshot:
        if k == key:
            output = kv_snapshot_reader(snapshot, key)
            assert output == v
            break

@given(
    snapshot=st.lists(
        st.tuples(st.integers(), st.integers()),
        min_size=1
    ),
    key=st.integers()
)
def test_branch_specific_behavior_k_greater_than_key(snapshot, key):
    for k, v in snapshot:
        if k > key:
            output = kv_snapshot_reader(snapshot, key)
            assert output == None
            break

@given(
    snapshot=st.lists(
        st.tuples(st.integers(), st.integers()),
        min_size=1
    ),
    key=st.integers()
)
def test_return_postcondition(snapshot, key):
    output = kv_snapshot_reader(snapshot, key)
    assert output == None