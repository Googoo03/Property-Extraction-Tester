import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.shard_assignment import shard_assignment

@given(keys=st.lists(st.text()), shards=st.integers(min_value=1, max_value=100))
def test_preserves_length(keys, shards):
    output = shard_assignment(keys, shards=shards)
    assert len(output) == len(keys)

@given(shards=st.integers(max_value=0))
def test_branch_specific_behavior(shards):
    with hypothesis.raises(ValueError):
        shard_assignment([], shards=shards)

@given(keys=st.lists(st.text()), shards=st.integers(min_value=1, max_value=100))
def test_loop_invariant_sum_length(keys, shards):
    buckets = shard_assignment(keys, shards=shards)
    assert sum(len(b) for b in buckets) == len(keys)

@given(keys=st.lists(st.text()), shards=st.integers(min_value=1, max_value=100))
def test_loop_invariant_all_keys_present(keys, shards):
    buckets = shard_assignment(keys, shards=shards)
    assert all(key in keys for bucket in buckets for key in bucket)

@given(keys=st.lists(st.text()), shards=st.integers(min_value=1, max_value=100))
def test_return_postcondition(keys, shards):
    output = shard_assignment(keys, shards=shards)
    assert len(output) == shards and all(isinstance(bucket, list) for bucket in output)