import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.divide_refund import divide_refund

# Property: preserves_length
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1))
def test_preserves_length(amount, ratios):
    output = divide_refund(amount, ratios)
    assert len(output) == len(ratios)

# Property: branch_specific_behavior (empty ratios)
def test_branch_specific_behavior_empty_ratios():
    with pytest.raises(ValueError, match="empty ratios"):
        divide_refund(100, [])

# Property: branch_specific_behavior (sum(ratios) <= 0)
def test_branch_specific_behavior_invalid_ratios():
    with pytest.raises(ValueError, match="invalid ratios"):
        divide_refund(100, [0, 0])

# Property: branch_specific_behavior (amount < 0)
def test_branch_specific_behavior_negative_amount():
    with pytest.raises(ValueError, match="negative amount"):
        divide_refund(-100, [1, 1])

# Property: return_postcondition
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1), fee=st.floats())
def test_return_postcondition(amount, ratios, fee):
    output = divide_refund(amount, ratios, fee=fee)
    assert all(b >= -fee for b in output)
    assert abs(sum(output) - (amount - fee)) < 1e-9

# Property: loop_invariant
@given(amount=st.floats(min_value=0), ratios=st.lists(st.floats(min_value=0), min_size=1))
def test_loop_invariant(amount, ratios):
    total_ratio = sum(ratios)
    output = divide_refund(amount, ratios)
    for i, b in enumerate(output):
        assert abs(b - ((ratios[i] / total_ratio) * amount)) < 1e-9