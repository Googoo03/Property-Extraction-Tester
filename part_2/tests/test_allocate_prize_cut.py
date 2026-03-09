import pytest
from hypothesis import given
from hypothesis import strategies as st
from dataset.python_programs.allocate_prize_cut import allocate_prize_cut

# Property: preserves_length
@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01), min_size=1, max_size=10))
def test_preserves_length(amount, ratios):
    output = allocate_prize_cut(amount, ratios)
    assert len(output) == len(ratios)

# Property: branch_specific_behavior (not ratios)
@given(amount=st.floats(min_value=0, max_value=1e6))
def test_branch_specific_behavior_not_ratios(amount):
    with pytest.raises(ValueError, match="ratios required"):
        allocate_prize_cut(amount, [])

# Property: branch_specific_behavior (amount < 0)
@given(ratios=st.lists(st.floats(min_value=0.01), min_size=1, max_size=10))
def test_branch_specific_behavior_amount_less_than_zero(ratios):
    with pytest.raises(ValueError, match="negative amount"):
        allocate_prize_cut(-1.0, ratios)

# Property: branch_specific_behavior (total_ratio <= 0)
@given(amount=st.floats(min_value=0, max_value=1e6))
def test_branch_specific_behavior_total_ratio_less_than_or_equal_zero(amount):
    with pytest.raises(ValueError, match="invalid ratios"):
        allocate_prize_cut(amount, [0, 0])

# Property: loop_invariant (all(r >= 0 for r in ratios) implies all(s >= 0 for s in shares))
@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0), min_size=1, max_size=10))
def test_loop_invariant_all_ratios_non_negative_implies_all_shares_non_negative(amount, ratios):
    if all(r >= 0 for r in ratios):
        output = allocate_prize_cut(amount, ratios)
        assert all(s >= 0 for s in output)

# Property: return_postcondition
@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01), min_size=1, max_size=10))
def test_return_postcondition(amount, ratios):
    output = allocate_prize_cut(amount, ratios)
    total_ratio = sum(ratios)
    expected = [(r / total_ratio) * amount - 0.0 for r in ratios]
    assert all(abs(s - e) < 1e-6 for s, e in zip(output, expected))

# Property: loop_invariant (sum(shares) == amount)
@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01), min_size=1, max_size=10))
def test_loop_invariant_sum_shares_equals_amount(amount, ratios):
    output = allocate_prize_cut(amount, ratios)
    assert abs(sum(output) - amount) < 1e-6