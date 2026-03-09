import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.normalize import normalize

@given(xs=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_preserve_length(xs):
    result = normalize(xs)
    assert len(result) == len(xs)

@given(xs=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior(xs):
    if len(xs) == 0:
        result = normalize(xs)
        assert result == []

@given(xs=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_return_postcondition_semantic_rule(xs):
    if len(xs) == 0:
        expected = xs
    else:
        s = sum(xs)
        expected = [x / s for x in xs]
    result = normalize(xs)
    assert result == expected

@given(xs=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_return_postcondition_conditional(xs):
    if len(xs) > 0:
        s = sum(xs)
        expected = [x / s for x in xs]
    else:
        expected = []
    result = normalize(xs)
    assert result == expected

@given(xs=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_loop_invariant(xs):
    if len(xs) > 0:
        s = sum(xs)
        result = normalize(xs)
        assert all(abs(result[i] * s - xs[i]) < 1e-9 for i in range(len(xs)))