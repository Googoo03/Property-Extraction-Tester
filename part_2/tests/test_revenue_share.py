import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.revenue_share import revenue_share

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=10),
       fee=st.floats(min_value=0, max_value=1e6))
def test_preserves_length(amount, ratios, fee):
    output = revenue_share(amount, ratios, fee=fee)
    assert len(output) == len(ratios)

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=0, max_size=0),
       fee=st.floats(min_value=0, max_value=1e6))
def test_branch_specific_behavior_empty_ratios(amount, ratios, fee):
    with pytest.raises(ValueError, match="ratios required"):
        revenue_share(amount, ratios, fee=fee)

@given(amount=st.floats(max_value=-1e-6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=10),
       fee=st.floats(min_value=0, max_value=1e6))
def test_branch_specific_behavior_negative_amount(amount, ratios, fee):
    with pytest.raises(ValueError, match="negative amount"):
        revenue_share(amount, ratios, fee=fee)

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(max_value=-1e-6), min_size=1, max_size=10),
       fee=st.floats(min_value=0, max_value=1e6))
def test_branch_specific_behavior_invalid_ratios(amount, ratios, fee):
    with pytest.raises(ValueError, match="invalid ratios"):
        revenue_share(amount, ratios, fee=fee)

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=10),
       fee=st.floats(min_value=0, max_value=1e6))
def test_loop_invariant_sum_shares(amount, ratios, fee):
    output = revenue_share(amount, ratios, fee=fee)
    assert sum(output) == amount - len(ratios) * fee

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=10),
       fee=st.floats(min_value=0, max_value=1e6))
def test_return_postcondition(amount, ratios, fee):
    output = revenue_share(amount, ratios, fee=fee)
    total_ratio = sum(ratios)
    for s, r in zip(output, ratios):
        assert s == (r / total_ratio) * amount - fee

@given(amount=st.floats(min_value=0, max_value=1e6),
       ratios=st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=10),
       fee=st.floats(min_value=0, max_value=1e6))
def test_loop_invariant_non_negative_shares(amount, ratios, fee):
    output = revenue_share(amount, ratios, fee=fee)
    assert all(s >= 0 for s in output)