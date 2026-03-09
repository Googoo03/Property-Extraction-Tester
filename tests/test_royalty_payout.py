import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.royalty_payout import royalty_payout

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100))
def test_preserves_length(amount, ratios):
    output = royalty_payout(amount, ratios)
    assert len(output) == len(ratios)

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100))
def test_branch_specific_behavior_not_ratios(amount, ratios):
    with pytest.raises(ValueError, match="ratios required"):
        royalty_payout(amount, [])

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100))
def test_branch_specific_behavior_amount_less_than_zero(amount, ratios):
    with pytest.raises(ValueError, match="negative amount"):
        royalty_payout(-1, ratios)

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100))
def test_branch_specific_behavior_total_ratio_less_than_or_equal_to_zero(amount, ratios):
    with pytest.raises(ValueError, match="invalid ratios"):
        royalty_payout(amount, [0, 0])

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100))
def test_loop_invariant(amount, ratios):
    output = royalty_payout(amount, ratios)
    assert all(s >= 0 for s in output) and sum(output) == amount - len(ratios) * 0.0

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100), fee=st.floats(min_value=0, max_value=1e6))
def test_return_postcondition(amount, ratios, fee):
    output = royalty_payout(amount, ratios, fee=fee)
    assert all(s >= -fee for s in output) and sum(output) == amount - len(ratios) * fee