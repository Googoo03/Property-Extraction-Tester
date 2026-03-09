import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.rebate_splitter import rebate_splitter

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_preserves_length(amount, ratios):
    output = rebate_splitter(amount, ratios)
    assert len(output) == len(ratios)

def test_branch_specific_behavior_no_ratios():
    with pytest.raises(ValueError, match="no ratios"):
        rebate_splitter(100, [])

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_invalid_ratios(ratios):
    with pytest.raises(ValueError, match="invalid ratios"):
        rebate_splitter(100, ratios)

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_negative_amount(amount, ratios):
    with pytest.raises(ValueError, match="negative amount"):
        rebate_splitter(amount, ratios)

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1))
def test_loop_invariant(amount, ratios):
    total_ratio = sum(ratios)
    base = [(r / total_ratio) * amount for r in ratios]
    assert all(base[i] == (ratios[i] / total_ratio) * amount for i in range(len(ratios)))

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), fee=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition(amount, ratios, fee):
    output = rebate_splitter(amount, ratios, fee=fee)
    total_ratio = sum(ratios)
    expected = [(r / total_ratio) * amount - fee for r in ratios]
    assert all(abs(output[i] - expected[i]) < 1e-9 for i in range(len(ratios)))

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_loop_invariant_base_calculation(amount, ratios):
    total_ratio = sum(ratios)
    base = [(r / total_ratio) * amount for r in ratios]
    assert all(base[i] == (ratios[i] / total_ratio) * amount for i in range(len(ratios)))