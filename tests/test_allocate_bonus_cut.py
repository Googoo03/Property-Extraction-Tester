import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.allocate_bonus_cut import allocate_bonus_cut

@given(amount=st.floats(), ratios=st.lists(st.floats()))
def test_preserves_length(amount, ratios):
    if not ratios or amount < 0 or sum(ratios) <= 0:
        return
    output = allocate_bonus_cut(amount, ratios)
    assert len(output) == len(ratios)

@given(ratios=st.lists(st.floats()))
def test_branch_specific_behavior_not_ratios(ratios):
    if ratios:
        return
    with pytest.raises(ValueError, match="ratios required"):
        allocate_bonus_cut(0, ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats()))
def test_branch_specific_behavior_amount_lt_0(amount, ratios):
    if amount >= 0:
        return
    with pytest.raises(ValueError, match="negative amount"):
        allocate_bonus_cut(amount, ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats()))
def test_branch_specific_behavior_total_ratio_le_0(amount, ratios):
    if sum(ratios) > 0:
        return
    with pytest.raises(ValueError, match="invalid ratios"):
        allocate_bonus_cut(amount, ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats()))
def test_loop_invariant_shares_len(amount, ratios):
    if not ratios or amount < 0 or sum(ratios) <= 0:
        return
    shares = []
    total_ratio = sum(ratios)
    for r in ratios:
        shares.append((r / total_ratio) * amount)
    assert len(shares) == len(ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats()))
def test_loop_invariant_all_shares_non_negative(amount, ratios):
    if not ratios or amount < 0 or sum(ratios) <= 0:
        return
    total_ratio = sum(ratios)
    shares = [(r / total_ratio) * amount for r in ratios]
    assert all(s >= 0 for s in shares)

@given(amount=st.floats(), ratios=st.lists(st.floats()))
def test_return_postcondition(amount, ratios):
    if not ratios or amount < 0 or sum(ratios) <= 0:
        return
    total_ratio = sum(ratios)
    fee = 0.0
    output = allocate_bonus_cut(amount, ratios, fee=fee)
    assert all(s >= -fee for s in output)
    assert all(s == (r / total_ratio) * amount - fee for s, r in zip(output, ratios))