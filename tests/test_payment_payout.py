import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.payment_payout import payment_payout

# Test for preserving length of output compared to input
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1))
def test_preserves_length(amount, ratios):
    output = payment_payout(amount, ratios)
    assert len(output) == len(ratios)

# Test for behavior when ratios is empty
def test_ratios_empty():
    with pytest.raises(ValueError):
        payment_payout(100, [])

# Test for behavior when amount is negative
def test_amount_negative():
    with pytest.raises(ValueError):
        payment_payout(-100, [1, 2, 3])

# Test for behavior when total_ratio is non-positive
def test_total_ratio_non_positive():
    with pytest.raises(ValueError):
        payment_payout(100, [0, 0, 0])

# Test for loop invariant: shares are computed as (r / total_ratio) * amount
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1))
def test_loop_invariant(amount, ratios):
    total_ratio = sum(ratios)
    if total_ratio > 0:
        output = payment_payout(amount, ratios)
        for i, r in enumerate(ratios):
            expected = (r / total_ratio) * amount - 0.0
            assert abs(output[i] - expected) < 1e-6

# Test for return postcondition: returns value satisfying expected semantics
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1))
def test_return_postcondition(amount, ratios):
    output = payment_payout(amount, ratios, fee=0.0)
    assert all(s >= 0 for s in output)

# Test for behavior when amount is zero
@given(ratios=st.lists(st.floats(min_value=0), min_size=1))
def test_amount_zero(ratios):
    output = payment_payout(0, ratios)
    assert all(s == 0 for s in output)

# Test for behavior when len(ratios) is one
@given(amount=st.floats(min_value=0))
def test_single_ratio(amount):
    output = payment_payout(amount, [1])
    assert output == [amount]

# Test for loop invariant: shares are non-negative if amount >= 0 and ratios are non-negative
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1))
def test_shares_non_negative(amount, ratios):
    total_ratio = sum(ratios)
    if total_ratio > 0:
        output = payment_payout(amount, ratios)
        assert all(s >= 0 for s in output)

# Test for return postcondition: sum of output equals amount minus total fee
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1), fee=st.floats(min_value=0))
def test_sum_of_output(amount, ratios, fee):
    output = payment_payout(amount, ratios, fee=fee)
    expected_sum = amount - (fee * len(ratios))
    assert abs(sum(output) - expected_sum) < 1e-6