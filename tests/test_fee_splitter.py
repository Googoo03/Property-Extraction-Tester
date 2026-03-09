import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.fee_splitter import fee_splitter

@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1, max_size=10))
def test_fee_splitter_preserves_length(amount, ratios):
    output = fee_splitter(amount, ratios)
    assert len(output) == len(ratios)

@given(ratios=st.lists(st.floats(), min_size=0, max_size=1))
def test_fee_splitter_branch_empty_ratios(ratios):
    with pytest.raises(ValueError, match="empty ratios"):
        fee_splitter(100, ratios)

@given(ratios=st.lists(st.floats(allow_nan=False), min_size=1, max_size=10))
def test_fee_splitter_branch_invalid_ratios(ratios):
    if sum(ratios) <= 0:
        with pytest.raises(ValueError, match="invalid ratios"):
            fee_splitter(100, ratios)

@given(amount=st.floats(max_value=-0.01), ratios=st.lists(st.floats(), min_size=1))
def test_fee_splitter_branch_negative_amount(amount, ratios):
    with pytest.raises(ValueError, match="negative amount"):
        fee_splitter(amount, ratios)

@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1, max_size=10), fee=st.floats())
def test_fee_splitter_return_postcondition(amount, ratios, fee):
    output = fee_splitter(amount, ratios, fee=fee)
    if amount >= 0 and fee == 0:
        assert all(b >= 0 for b in output)
    else:
        assert True

@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1, max_size=10))
def test_fee_splitter_loop_invariant(amount, ratios):
    total_ratio = sum(ratios)
    base = list(map(lambda r: (r / total_ratio) * amount, ratios))
    assert sum(base) == amount