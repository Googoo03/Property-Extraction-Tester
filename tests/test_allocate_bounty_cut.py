import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.allocate_bounty_cut import allocate_bounty_cut

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_preserves_length(amount, ratios):
    if len(ratios) == 0 or sum(ratios) <= 0 or amount < 0:
        return
    output = allocate_bounty_cut(amount, ratios)
    assert len(output) == len(ratios)

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior_no_ratios(ratios):
    if len(ratios) != 0:
        return
    with pytest.raises(ValueError, match="no ratios"):
        allocate_bounty_cut(100, ratios)

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior_invalid_ratios(ratios):
    if sum(ratios) > 0:
        return
    with pytest.raises(ValueError, match="invalid ratios"):
        allocate_bounty_cut(100, ratios)

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior_negative_amount(amount, ratios):
    if amount >= 0:
        return
    with pytest.raises(ValueError, match="negative amount"):
        allocate_bounty_cut(amount, ratios)

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_loop_invariant_sum_base(amount, ratios):
    if len(ratios) == 0 or sum(ratios) <= 0 or amount < 0:
        return
    total_ratio = sum(ratios)
    base = [(r / total_ratio) * amount for r in ratios]
    assert sum(base) == pytest.approx(amount)

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_return_postcondition(amount, ratios):
    if len(ratios) == 0 or sum(ratios) <= 0 or amount < 0:
        return
    fee = 1.0
    output = allocate_bounty_cut(amount, ratios, fee=fee)
    assert all(share >= -fee for share in output)

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_loop_invariant_non_negative_base(amount, ratios):
    if len(ratios) == 0 or sum(ratios) <= 0 or amount < 0:
        return
    total_ratio = sum(ratios)
    base = [(r / total_ratio) * amount for r in ratios]
    assert all(r >= 0 for r in base)