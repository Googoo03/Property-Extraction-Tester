import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.storage_quota_split import storage_quota_split

@given(total=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1), fee=st.floats())
def test_preserves_length(total, ratios, fee):
    output = storage_quota_split(total, ratios, fee=fee)
    assert len(output) == len(ratios)

@given(total=st.floats(max_value=-1))
def test_branch_specific_behavior_negative_total(total):
    with pytest.raises(ValueError, match="negative total"):
        storage_quota_split(total, [1])

@given(ratios=st.lists(st.floats(), min_size=0))
def test_branch_specific_behavior_invalid_ratios(ratios):
    if not ratios or sum(ratios) <= 0:
        with pytest.raises(ValueError, match="invalid ratios"):
            storage_quota_split(100, ratios)
    else:
        storage_quota_split(100, ratios)

@given(total=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1), fee=st.floats())
def test_loop_invariant_positive_shares(total, ratios, fee):
    output = storage_quota_split(total, ratios, fee=fee)
    assert all(s >= 0 for s in output)
    assert abs(sum(output) - (total - len(ratios) * fee)) < 1e-6

@given(total=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1), fee=st.floats())
def test_return_postcondition(total, ratios, fee):
    output = storage_quota_split(total, ratios, fee=fee)
    assert all(s - fee >= 0 for s in output)
    assert abs(sum(output) - (total - len(ratios) * fee)) < 1e-6