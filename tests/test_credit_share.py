import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.credit_share import credit_share

# Test for preserving length property
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0.1), min_size=1))
def test_preserves_length(amount, ratios):
    output = credit_share(amount, ratios)
    assert len(output) == len(ratios)

# Test for branch-specific behavior when ratios is empty
def test_branch_specific_behavior_ratios_empty():
    with pytest.raises(ValueError, match="ratios required"):
        credit_share(100, [])

# Test for branch-specific behavior when amount is negative
def test_branch_specific_behavior_amount_negative():
    with pytest.raises(ValueError, match="negative amount"):
        credit_share(-100, [1, 1])

# Test for branch-specific behavior when total_ratio is non-positive
def test_branch_specific_behavior_total_ratio_non_positive():
    with pytest.raises(ValueError, match="invalid ratios"):
        credit_share(100, [0, 0])

# Test for loop invariant: all shares are non-negative if amount is non-negative and total_ratio is positive
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0.1), min_size=1))
def test_loop_invariant_non_negative_shares(amount, ratios):
    shares = credit_share(amount, ratios)
    assert all(s >= 0 for s in shares)

# Test for return postcondition: shares are adjusted by fee and match expected formula
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0.1), min_size=1), fee=st.floats())
def test_return_postcondition(amount, ratios, fee):
    output = credit_share(amount, ratios, fee=fee)
    total_ratio = sum(ratios)
    assert all(s >= -fee for s in output)
    assert all(s == (r / total_ratio) * amount - fee for s, r in zip(output, ratios))

# Test for loop invariant: sum of shares equals amount minus total fee
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0.1), min_size=1), fee=st.floats())
def test_loop_invariant_sum_of_shares(amount, ratios, fee):
    shares = credit_share(amount, ratios, fee=fee)
    total_ratio = sum(ratios)
    if fee == 0:
        assert sum(shares) == amount
    else:
        assert sum(shares) == amount - len(ratios) * fee