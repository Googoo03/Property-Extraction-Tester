# test_normalize.py
# Hypothesis‑driven tests for the `normalize` function.
# Assumes the function is defined in `dataset/python_programs/normalize.py`.

import math
from typing import List

import pytest
from hypothesis import given, assume, strategies as st

# Import the function under test.
# Adjust the import path if your package layout differs.
from dataset.python_programs.normalize import normalize


# ----------------------------------------------------------------------
# Helper strategies
# ----------------------------------------------------------------------
def number():
    """A strategy for real numbers (int or float) without NaN/Inf."""
    return st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False, width=32),
    )


def number_list():
    """A strategy for a list of numbers (the precondition for all tests)."""
    return st.lists(elements=number(), min_size=0, max_size=20)


# ----------------------------------------------------------------------
# Property: preserves_length
# ----------------------------------------------------------------------
@given(xs=number_list())
def test_preserves_length(xs: List[float]):
    """The output list must have the same length as the input list."""
    # Precondition: xs is a list of numbers (already guaranteed by the strategy)
    assume(isinstance(xs, list) and all(isinstance(x, (int, float)) for x in xs))

    output = normalize(xs)
    assert isinstance(output, list)
    assert len(output) == len(xs)


# ----------------------------------------------------------------------
# Property: branch_specific_behavior (len(xs) == 0)
# ----------------------------------------------------------------------
@given(xs=number_list())
def test_branch_specific_behavior(xs: List[float]):
    """When the input list is empty, the function should return the same empty list."""
    assume(isinstance(xs, list) and all(isinstance(x, (int, float)) for x in xs))
    assume(len(xs) == 0)  # branch condition

    output = normalize(xs)
    assert output == xs


# ----------------------------------------------------------------------
# Property: return_postcondition_empty
# ----------------------------------------------------------------------
@given(xs=number_list())
def test_return_postcondition_empty(xs: List[float]):
    """Empty input → empty output."""
    assume(isinstance(xs, list) and all(isinstance(x, (int, float)) for x in xs))
    assume(len(xs) == 0)

    output = normalize(xs)
    assert output == xs


# ----------------------------------------------------------------------
# Property: return_postcondition_nonempty
# ----------------------------------------------------------------------
@given(xs=number_list())
def test_return_postcondition_nonempty(xs: List[float]):
    """Non‑empty input with non‑zero sum → each element divided by the total sum."""
    assume(isinstance(xs, list) and all(isinstance(x, (int, float)) for x in xs))
    assume(len(xs) > 0)
    total = sum(xs)
    assume(total != 0)

    output = normalize(xs)
    expected = [x / total for x in xs]

    assert isinstance(output, list)
    assert len(output) == len(expected)
    for o, e in zip(output, expected):
        # Use a tolerant comparison for floating‑point values.
        assert math.isclose(o, e, rel_tol=1e-9, abs_tol=0.0)


# ----------------------------------------------------------------------
# Property: loop_invariant
# ----------------------------------------------------------------------
@given(xs=number_list())
def test_loop_invariant(xs: List[float]):
    """
    For each prefix i, the sum of the first i output elements should equal
    the sum of the first i input elements divided by the total sum of the input.
    """
    assume(isinstance(xs, list) and all(isinstance(x, (int, float)) for x in xs))
    assume(len(xs) > 0)
    total = sum(xs)
    assume(total != 0)

    output = normalize(xs)

    # Verify the invariant for every prefix.
    for i in range(1, len(xs) + 1):
        prefix_output_sum = sum(output[:i])
        prefix_input_sum = sum(xs[:i]) / total
        assert abs(prefix_output_sum - prefix_input_sum) < 1e-9