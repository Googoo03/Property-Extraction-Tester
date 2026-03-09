# test_normalize.py
import math
import pytest
from hypothesis import given, strategies as st, assume

# Adjust the import path according to your project layout.
# It is assumed that the function `normalize` resides in
# `dataset/python_programs/normalize.py`.
from dataset.python_programs.normalize import normalize


# Helper strategy for a list of numeric values (int or float)
numeric_list = st.lists(
    st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
    ),
    min_size=0,
)


@given(xs=numeric_list)
def test_preserves_length(xs):
    """Property: preserves_length"""
    # precondition
    assume(isinstance(xs, list) and all(isinstance(x, (int, float)) for x in xs))
    output = normalize(xs)
    assert len(output) == len(xs)


@given(xs=numeric_list)
def test_branch_specific_behavior(xs):
    """Property: branch_specific_behavior when len(xs) == 0"""
    # precondition
    assume(isinstance(xs, list) and all(isinstance(x, (int, float)) for x in xs))
    assume(len(xs) == 0)
    output = normalize(xs)
    assert output == []


def test_return_postcondition_empty():
    """Property: return_postcondition for empty input"""
    xs = []
    # precondition is xs == []
    output = normalize(xs)
    assert output == []


@given(xs=numeric_list)
def test_return_postcondition_normal(xs):
    """Property: return_postcondition for non‑empty list with non‑zero sum"""
    # precondition
    assume(len(xs) > 0)
    total = sum(xs)
    assume(total != 0)
    output = normalize(xs)
    expected = [x / total for x in xs]
    # Use isclose for floating‑point comparison
    assert len(output) == len(expected)
    for o, e in zip(output, expected):
        assert math.isclose(o, e, rel_tol=1e-9, abs_tol=0.0)


@given(xs=numeric_list)
def test_loop_invariant(xs):
    """Property: loop_invariant – the sum of the normalized list equals 1"""
    # precondition
    assume(len(xs) > 0)
    total = sum(xs)
    assume(total != 0)
    output = normalize(xs)
    # Guard against empty output in case of unexpected implementation
    assume(len(output) > 0)
    assert math.isclose(sum(output), 1.0, rel_tol=1e-9, abs_tol=0.0)