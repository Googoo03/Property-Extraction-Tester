import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.divide_coupon import divide_coupon

# Property: preserves_length
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    ratios=st.lists(st.floats(min_value=0.1, max_value=1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_preserves_length(amount, ratios, fee):
    output = divide_coupon(amount, ratios, fee=fee)
    assert len(output) == len(ratios)

# Property: branch_specific_behavior (empty ratios)
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_branch_empty_ratios(amount, fee):
    with pytest.raises(ValueError, match="empty ratios"):
        divide_coupon(amount, [], fee=fee)

# Property: branch_specific_behavior (sum(ratios) <= 0)
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_branch_sum_ratios_le_zero(amount, fee):
    with pytest.raises(ValueError, match="invalid ratios"):
        divide_coupon(amount, [0, 0], fee=fee)

# Property: branch_specific_behavior (amount < 0)
@given(
    ratios=st.lists(st.floats(min_value=0.1, max_value=1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_branch_amount_negative(ratios, fee):
    with pytest.raises(ValueError, match="negative amount"):
        divide_coupon(-1.0, ratios, fee=fee)

# Property: return_postcondition
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    ratios=st.lists(st.floats(min_value=0.1, max_value=1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_return_postcondition(amount, ratios, fee):
    output = divide_coupon(amount, ratios, fee=fee)
    assert all(b >= -fee for b in output)

# Property: loop_invariant
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    ratios=st.lists(st.floats(min_value=0.1, max_value=1e6), min_size=1, max_size=100)
)
def test_loop_invariant(amount, ratios):
    base = list(map(lambda r: (r / sum(ratios)) * amount, ratios))
    assert sum(base) == amount