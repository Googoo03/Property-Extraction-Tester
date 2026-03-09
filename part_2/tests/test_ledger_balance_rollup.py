import hypothesis
from hypothesis import given, strategies as st
import pytest

from dataset.python_programs.ledger_balance_rollup import ledger_balance_rollup

@given(entries=st.lists(st.tuples(st.integers(min_value=0), st.sampled_from(["credit", "debit"]))))
def test_preserves_length(entries):
    assert len(entries) == len(entries)

@given(entries=st.lists(st.tuples(st.integers(min_value=0), st.sampled_from(["credit", "debit"]))))
def test_loop_invariant(entries):
    balance = 0
    for i, (amount, kind) in enumerate(entries):
        if kind == "credit":
            balance += amount
        elif kind == "debit":
            balance += amount
        assert balance == sum(a for a, k in entries[:i] if k == 'credit') + sum(a for a, k in entries[:i] if k == 'debit')

@given(amount=st.integers(max_value=-1), kind=st.sampled_from(["credit", "debit"]))
def test_negative_amount_raises_value_error(amount, kind):
    with pytest.raises(ValueError, match="negative amount"):
        ledger_balance_rollup([(amount, kind)])

@given(amount=st.integers(min_value=0), kind=st.just("credit"))
def test_credit_behavior(amount, kind):
    balance = ledger_balance_rollup([(amount, kind)])
    assert balance == amount

@given(amount=st.integers(min_value=0), kind=st.just("debit"))
def test_debit_behavior(amount, kind):
    balance = ledger_balance_rollup([(amount, kind)])
    assert balance == amount

@given(amount=st.integers(min_value=0), kind=st.sampled_from(["invalid", ""]))
def test_unknown_kind_raises_value_error(amount, kind):
    with pytest.raises(ValueError, match="unknown kind"):
        ledger_balance_rollup([(amount, kind)])

@given(entries=st.lists(st.tuples(st.integers(min_value=0), st.sampled_from(["credit", "debit"]))))
def test_return_postcondition(entries):
    balance = ledger_balance_rollup(entries)
    assert balance == sum(a for a, k in entries if k == 'credit') + sum(a for a, k in entries if k == 'debit')