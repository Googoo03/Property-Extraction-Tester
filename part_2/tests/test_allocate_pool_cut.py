import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.allocate_pool_cut import allocate_pool_cut

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_preserves_length(amount, ratios):
    try:
        output = allocate_pool_cut(amount, ratios)
        assert len(output) == len(ratios)
    except ValueError:
        pass

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior_not_ratios(ratios):
    with pytest.raises(ValueError, match="ratios required"):
        allocate_pool_cut(100, [])

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior_amount_less_than_zero(amount, ratios):
    if amount < 0:
        with pytest.raises(ValueError, match="negative amount"):
            allocate_pool_cut(amount, ratios)

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior_total_ratio_less_than_or_equal_zero(amount, ratios):
    if sum(ratios) <= 0:
        with pytest.raises(ValueError, match="invalid ratios"):
            allocate_pool_cut(amount, ratios)

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False, min_value=0)))
def test_loop_invariant_non_negative_ratios(ratios):
    try:
        amount = 100
        output = allocate_pool_cut(amount, ratios)
        assert all(s >= 0 for s in output)
    except ValueError:
        pass

@given(amount=st.floats(allow_nan=False, allow_infinity=False), ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_return_postcondition(amount, ratios):
    try:
        output = allocate_pool_cut(amount, ratios)
        assert all(s >= -0.0 for s in output)
    except ValueError:
        pass

@given(ratios=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_loop_invariant_sum_of_shares(ratios):
    try:
        amount = 100
        output = allocate_pool_cut(amount, ratios)
        assert abs(sum(output) - amount) < 1e-9
    except ValueError:
        pass