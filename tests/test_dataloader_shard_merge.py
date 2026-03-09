from hypothesis import given
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, precondition
#from hypothesis.extra.orderedset import ordered_set

def dataloader_shard_merge(left_ids, right_ids):
    i = j = 0
    merged = []
    while i < len(left_ids) and j < len(right_ids):
        if left_ids[i] <= right_ids[j]:
            merged.append(left_ids[i])
            i += 1
        else:
            merged.append(right_ids[j])
            j += 1
    merged.extend(left_ids[i:])
    merged.extend(right_ids[j:])

    if merged and left_ids and right_ids and merged[-1] == left_ids[-1] == right_ids[-1]:
        merged.pop()
    return merged

class DataloaderShardMergeTests(RuleBasedStateMachine):
    @rule(left_ids=st.lists(st.integers()), right_ids=st.lists(st.integers()))
    def test_preserves_length(self, left_ids, right_ids):
        output = dataloader_shard_merge(left_ids, right_ids)
        assert len(output) == len(left_ids) + len(right_ids)

    @rule(left_ids=st.lists(st.integers()), right_ids=st.lists(st.integers()))
    def test_loop_invariant(self, left_ids, right_ids):
        i = j = 0
        merged = []
        while i < len(left_ids) and j < len(right_ids):
            if left_ids[i] <= right_ids[j]:
                merged.append(left_ids[i])
                i += 1
            else:
                merged.append(right_ids[j])
                j += 1
            assert all(merged[:i+j] == sorted(left_ids[:i] + right_ids[:j]))

    @rule(left_ids=st.lists(st.integers()), right_ids=st.lists(st.integers()))
    def test_branch_specific_behavior(self, left_ids, right_ids):
        i = j = 0
        merged = []
        while i < len(left_ids) and j < len(right_ids):
            if left_ids[i] <= right_ids[j]:
                merged.append(left_ids[i])
                i += 1
            else:
                merged.append(right_ids[j])
                j += 1
            assert merged[i+j-1] == (left_ids[i-1] if left_ids[i-1] <= right_ids[j-1] else right_ids[j-1])

    @rule(left_ids=st.lists(st.integers()), right_ids=st.lists(st.integers()))
    def test_branch_specific_behavior_bug(self, left_ids, right_ids):
        output = dataloader_shard_merge(left_ids, right_ids)
        if output and left_ids and right_ids and output[-1] == left_ids[-1] == right_ids[-1]:
            assert output[-1] != left_ids[-1]
        else:
            assert output[-1] == left_ids[-1] or output[-1] == right_ids[-1]

    @rule(left_ids=st.lists(st.integers()), right_ids=st.lists(st.integers()))
    def test_return_postcondition(self, left_ids, right_ids):
        output = dataloader_shard_merge(left_ids, right_ids)
        assert all(output[i] <= output[i+1] for i in range(len(output)-1))
        assert set(output) == set(left_ids + right_ids)