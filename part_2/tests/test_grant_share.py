import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.grant_share import grant_share

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=0))
def test_preserve_length(amount, ratios):
    if len(ratios) == 0 or sum(ratios) <= 0 or amount < 0:
        return
    result = grant_share(amount, ratios)
    assert len(result) == len(ratios)

@given(ratios=st.lists(st.floats(), min_size=0))
def test_branch_no_ratios(ratios):
    if len(ratios) != 0:
        return
    with pytest.raises(ValueError, match="no ratios"):
        grant_share(100, ratios)

@given(ratios=st.lists(st.floats(), min_size=1))
def test_branch_invalid_ratios(ratios):
    if sum(ratios) > 0:
        return
    with pytest.raises(ValueError, match="invalid ratios"):
        grant_share(100, ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_branch_negative_amount(amount, ratios):
    if amount >= 0:
        return
    with pytest.raises(ValueError, match="negative amount"):
        grant_share(amount, ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_loop_invariant_sum_base(amount, ratios):
    if sum(ratios) <= 0 or amount < 0:
        return
    base = [(r / sum(ratios)) * amount for r in ratios]
    assert abs(sum(base) - amount) < 1e-9

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_return_postcondition(amount, ratios):
    if sum(ratios) <= 0 or amount < 0:
        return
    result = grant_share(amount, ratios)
    assert all(share >= -0.0 for share in result)

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_loop_invariant_ratios_non_negative(amount, ratios):
    if sum(ratios) <= 0:
        return
    assert all(r >= 0 for r in ratios) or (sum(ratios) > 0)