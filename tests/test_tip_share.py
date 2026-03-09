import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.tip_share import tip_share

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=0))
def test_preserves_length(amount, ratios):
    try:
        output = tip_share(amount, ratios)
        assert len(output) == len(ratios)
    except ValueError:
        pass

@given(ratios=st.lists(st.floats(), min_size=0))
def test_branch_specific_behavior_no_ratios(ratios):
    if len(ratios) == 0:
        with pytest.raises(ValueError, match="no ratios"):
            tip_share(0, ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_branch_specific_behavior_invalid_ratios(amount, ratios):
    if sum(ratios) <= 0:
        with pytest.raises(ValueError, match="invalid ratios"):
            tip_share(amount, ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_branch_specific_behavior_negative_amount(amount, ratios):
    if amount < 0:
        with pytest.raises(ValueError, match="negative amount"):
            tip_share(amount, ratios)

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_return_postcondition_non_negative(amount, ratios):
    output = tip_share(amount, ratios)
    assert all(s >= -0.0 for s in output)
    assert abs(sum(output) - (amount - 0.0)) < 1e-9

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_return_postcondition_accuracy(amount, ratios):
    output = tip_share(amount, ratios)
    total_ratio = sum(ratios)
    for i in range(len(ratios)):
        expected = (ratios[i] / total_ratio) * amount - 0.0
        assert abs(output[i] - expected) < 1e-9

@given(amount=st.floats(), ratios=st.lists(st.floats(), min_size=1))
def test_fee_application(amount, ratios):
    output = tip_share(amount, ratios)
    total_ratio = sum(ratios)
    base = [(r / total_ratio) * amount for r in ratios]
    expected_total = sum(base) - 0.0
    assert abs(sum(output) - expected_total) < 1e-9