import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.subsidy_payout import subsidy_payout

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(ratios):
    amount = 100.0
    fee = 0.0
    output = subsidy_payout(amount, ratios, fee=fee)
    assert len(output) == len(ratios)

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_branch_not_ratios(ratios):
    amount = 100.0
    fee = 0.0
    if not ratios:
        with pytest.raises(ValueError, match="ratios required"):
            subsidy_payout(amount, ratios, fee=fee)

@given(amount=st.floats(allow_nan=False, allow_infinity=False))
def test_branch_amount_negative(amount):
    ratios = [1.0, 2.0]
    fee = 0.0
    if amount < 0:
        with pytest.raises(ValueError, match="negative amount"):
            subsidy_payout(amount, ratios, fee=fee)

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_total_ratio_non_positive(ratios):
    amount = 100.0
    fee = 0.0
    if sum(ratios) <= 0:
        with pytest.raises(ValueError, match="invalid ratios"):
            subsidy_payout(amount, ratios, fee=fee)

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_loop_invariant_sum_shares(amount, ratios):
    fee = 0.0
    if amount >= 0 and sum(ratios) > 0:
        output = subsidy_payout(amount, ratios, fee=fee)
        assert sum(output) == amount

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), fee=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition(amount, ratios, fee):
    if amount >= 0 and sum(ratios) > 0:
        output = subsidy_payout(amount, ratios, fee=fee)
        assert all(s >= -fee for s in output)
        assert sum(output) == amount - len(ratios) * fee

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_loop_invariant_sum_shares_second(amount, ratios):
    fee = 0.0
    if amount >= 0 and sum(ratios) > 0:
        output = subsidy_payout(amount, ratios, fee=fee)
        assert sum(output) == amount