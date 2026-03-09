import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.payment_split_rebate import payment_split_rebate

@given(total=st.floats(min_value=0, allow_nan=False, allow_infinity=False),
       ratios=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
       rebate=st.floats(allow_nan=False, allow_infinity=False))
def test_preserves_length(total, ratios, rebate):
    output = payment_split_rebate(total, ratios, rebate=rebate)
    assert len(output) == len(ratios)

@given(total=st.floats(max_value=-0.01, allow_nan=False, allow_infinity=False))
def test_negative_total_raises_value_error(total):
    with pytest.raises(ValueError, match="negative total"):
        payment_split_rebate(total, [1.0])

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=0))
def test_empty_ratios_raises_value_error(ratios):
    with pytest.raises(ValueError, match="invalid ratios"):
        payment_split_rebate(100, ratios)

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_zero_sum_ratios_raises_value_error(ratios):
    if sum(ratios) <= 0:
        with pytest.raises(ValueError, match="invalid ratios"):
            payment_split_rebate(100, ratios)

@given(total=st.floats(min_value=0, allow_nan=False, allow_infinity=False),
       ratios=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
       rebate=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition(total, ratios, rebate):
    output = payment_split_rebate(total, ratios, rebate=rebate)
    assert sum(output) == total - rebate

@given(total=st.floats(min_value=0, allow_nan=False, allow_infinity=False),
       ratios=st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1),
       rebate=st.floats(allow_nan=False, allow_infinity=False))
def test_loop_invariant(total, ratios, rebate):
    output = payment_split_rebate(total, ratios, rebate=rebate)
    total_ratio = sum(ratios)
    for i, s in enumerate(output):
        assert s == (ratios[i] / total_ratio) * total - rebate