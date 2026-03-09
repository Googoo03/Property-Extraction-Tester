import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.allocate_budget_cut import allocate_budget_cut

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=10))
def test_preserve_length(amount, ratios):
    output = allocate_budget_cut(amount, ratios)
    assert len(output) == len(ratios)

@given(ratios=st.lists(st.floats(), min_size=0, max_size=0))
def test_raises_value_error_when_ratios_is_empty(ratios):
    with pytest.raises(ValueError):
        allocate_budget_cut(100, ratios)

@given(amount=st.floats(max_value=-0.01))
def test_raises_value_error_when_amount_is_negative(amount):
    with pytest.raises(ValueError):
        allocate_budget_cut(amount, [1.0])

@given(ratios=st.lists(st.floats(max_value=0), min_size=1, max_size=10))
def test_raises_value_error_when_total_ratio_is_non_positive(ratios):
    with pytest.raises(ValueError):
        allocate_budget_cut(100, ratios)

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=10))
def test_each_share_is_computed_as_r_over_total_ratio_times_amount(amount, ratios):
    total_ratio = sum(ratios)
    output = allocate_budget_cut(amount, ratios)
    for r, s in zip(ratios, output):
        assert abs(s + 0.0 - (r / total_ratio) * amount) < 1e-9

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=10))
def test_returns_shares_minus_fee(amount, ratios):
    output = allocate_budget_cut(amount, ratios)
    shares = [(r / sum(ratios)) * amount for r in ratios]
    expected = [s - 0.0 for s in shares]
    assert all(abs(o - e) < 1e-9 for o, e in zip(output, expected))

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=10))
def test_each_share_in_output_is_reduced_by_fee(amount, ratios):
    output = allocate_budget_cut(amount, ratios, fee=0.5)
    shares = [(r / sum(ratios)) * amount for r in ratios]
    expected = [s - 0.5 for s in shares]
    assert all(abs(o - e) < 1e-9 for o, e in zip(output, expected))

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=10))
def test_sum_of_output_shares_equals_amount_minus_fee_times_length(amount, ratios):
    output = allocate_budget_cut(amount, ratios, fee=0.5)
    expected_sum = amount - (0.5 * len(ratios))
    assert abs(sum(output) - expected_sum) < 1e-9

@given(amount=st.floats(min_value=0, max_value=1e6), ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=10))
def test_shares_are_proportional_to_input_ratios_before_fee_deduction(amount, ratios):
    output = allocate_budget_cut(amount, ratios, fee=0.0)
    shares = [(r / sum(ratios)) * amount for r in ratios]
    assert all(abs(o - e) < 1e-9 for o, e in zip(output, shares))