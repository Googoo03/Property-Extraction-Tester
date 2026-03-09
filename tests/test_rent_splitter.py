import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.rent_splitter import rent_splitter

# Property: preserves_length
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_preserves_length(amount, ratios, fee):
    result = rent_splitter(amount, ratios, fee=fee)
    assert len(result) == len(ratios)

# Property: branch_specific_behavior (len(ratios) == 0)
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_branch_specific_behavior_empty_ratios(amount, fee):
    with pytest.raises(ValueError, match="no ratios"):
        rent_splitter(amount, [], fee=fee)

# Property: branch_specific_behavior (sum(ratios) <= 0)
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    ratios=st.lists(st.floats(max_value=0, min_value=-1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_branch_specific_behavior_invalid_ratios(amount, ratios, fee):
    with pytest.raises(ValueError, match="invalid ratios"):
        rent_splitter(amount, ratios, fee=fee)

# Property: branch_specific_behavior (amount < 0)
@given(
    amount=st.floats(max_value=-0.01),
    ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_branch_specific_behavior_negative_amount(amount, ratios, fee):
    with pytest.raises(ValueError, match="negative amount"):
        rent_splitter(amount, ratios, fee=fee)

# Property: loop_invariant (each share is computed as (r / total_ratio) * amount)
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_loop_invariant_share_computation(amount, ratios, fee):
    total_ratio = sum(ratios)
    base = [(r / total_ratio) * amount for r in ratios]
    result = rent_splitter(amount, ratios, fee=fee)
    for i, share in enumerate(result):
        assert share == pytest.approx(base[i] - fee)

# Property: return_postcondition (returns value satisfying expected semantics)
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_return_postcondition(amount, ratios, fee):
    result = rent_splitter(amount, ratios, fee=fee)
    base = [(r / sum(ratios)) * amount for r in ratios]
    expected = [share - fee for share in base]
    assert all(r == pytest.approx(e) for r, e in zip(result, expected))

# Property: loop_invariant (sum of base shares equals amount before fee is applied)
@given(
    amount=st.floats(min_value=0, max_value=1e6),
    ratios=st.lists(st.floats(min_value=0.01, max_value=1e6), min_size=1, max_size=100),
    fee=st.floats(min_value=0, max_value=1e6)
)
def test_loop_invariant_sum_equals_amount(amount, ratios, fee):
    base = [(r / sum(ratios)) * amount for r in ratios]
    assert sum(base) == pytest.approx(amount)