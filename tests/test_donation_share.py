import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.donation_share import donation_share

@given(amount=st.floats(allow_nan=False, allow_infinity=False),
       ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False, min_value=0.0), min_size=1),
       fee=st.floats(allow_nan=False, allow_infinity=False))
def test_preserves_length(amount, ratios, fee):
    result = donation_share(amount, ratios, fee=fee)
    assert len(result) == len(ratios)

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=0))
def test_branch_empty_ratios(ratios):
    with pytest.raises(ValueError, match="empty ratios"):
        donation_share(100.0, ratios)

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6), min_size=1))
def test_branch_invalid_ratios(ratios):
    if sum(ratios) <= 0:
        with pytest.raises(ValueError, match="invalid ratios"):
            donation_share(100.0, ratios)

@given(amount=st.floats(allow_nan=False, allow_infinity=False, max_value=-0.01))
def test_branch_negative_amount(amount):
    with pytest.raises(ValueError, match="negative amount"):
        donation_share(amount, [1.0])

@given(amount=st.floats(allow_nan=False, allow_infinity=False, min_value=0.0),
       ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False, min_value=0.0), min_size=1),
       fee=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition(amount, ratios, fee):
    result = donation_share(amount, ratios, fee=fee)
    total_ratio = sum(ratios)
    expected = [(r / total_ratio) * amount - fee for r in ratios]
    assert all(hypothesis.functions.approx_eq(b, e) for b, e in zip(result, expected))

@given(amount=st.floats(allow_nan=False, allow_infinity=False, min_value=0.0),
       ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False, min_value=0.0), min_size=1),
       fee=st.floats(allow_nan=False, allow_infinity=False))
def test_loop_invariant(amount, ratios, fee):
    total_ratio = sum(ratios)
    result = donation_share(amount, ratios, fee=fee)
    expected = [(r / total_ratio) * amount for r in ratios]
    assert all(hypothesis.functions.approx_eq(b + fee, e) for b, e in zip(result, expected))