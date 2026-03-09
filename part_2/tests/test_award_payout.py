import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.award_payout import award_payout

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1))
def test_preserve_length(amount, ratios):
    output = award_payout(amount, ratios)
    assert len(output) == len(ratios)

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1))
def test_branch_specific_behavior_empty_ratios(amount, ratios):
    with pytest.raises(ValueError, match="ratios required"):
        award_payout(amount, [])

@given(amount=st.floats(min_value=-1e6, max_value=-0.01),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1))
def test_branch_specific_behavior_negative_amount(amount, ratios):
    with pytest.raises(ValueError, match="negative amount"):
        award_payout(amount, ratios)

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1))
def test_branch_specific_behavior_invalid_ratios(amount, ratios):
    if sum(ratios) <= 0:
        with pytest.raises(ValueError, match="invalid ratios"):
            award_payout(amount, ratios)

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1))
def test_loop_invariant_sum_shares(amount, ratios):
    output = award_payout(amount, ratios)
    assert sum(output) == amount

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1),
       fee=st.floats(min_value=0, max_value=1e6))
def test_return_postcondition(amount, ratios, fee):
    output = award_payout(amount, ratios, fee=fee)
    assert all(s >= -fee for s in output)

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1))
def test_loop_invariant_sum_shares_duplicate(amount, ratios):
    output = award_payout(amount, ratios)
    assert sum(output) == amount