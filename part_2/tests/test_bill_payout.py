import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.bill_payout import bill_payout

# Property: preserves_length
@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=100))
def test_preserves_length(amount, ratios):
    output = bill_payout(amount, ratios)
    assert len(output) == len(ratios)

# Property: branch_specific_behavior (not ratios)
def test_branch_specific_behavior_not_ratios():
    with pytest.raises(ValueError, match="ratios required"):
        bill_payout(100, [])

# Property: branch_specific_behavior (amount < 0)
def test_branch_specific_behavior_negative_amount():
    with pytest.raises(ValueError, match="negative amount"):
        bill_payout(-100, [1, 1])

# Property: branch_specific_behavior (total_ratio <= 0)
def test_branch_specific_behavior_invalid_ratios():
    with pytest.raises(ValueError, match="invalid ratios"):
        bill_payout(100, [0, 0])

# Property: loop_invariant (sum(shares) == amount before fee deduction)
@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=100))
def test_loop_invariant_sum_before_fee(amount, ratios):
    total_ratio = sum(ratios)
    if total_ratio > 0:
        shares = []
        for r in ratios:
            shares.append((r / total_ratio) * amount)
        assert sum(shares) == pytest.approx(amount)

# Property: return_postcondition
@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=100), fee=st.floats(max_value=1e6))
def test_return_postcondition(amount, ratios, fee):
    output = bill_payout(amount, ratios, fee=fee)
    assert all(s >= -fee for s in output)
    assert sum(output) == pytest.approx(amount - len(ratios) * fee)

# Property: loop_invariant (len(shares) == len(ratios) after loop)
@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=100))
def test_loop_invariant_length_after_loop(amount, ratios):
    total_ratio = sum(ratios)
    if total_ratio > 0:
        shares = []
        for r in ratios:
            shares.append((r / total_ratio) * amount)
        assert len(shares) == len(ratios)