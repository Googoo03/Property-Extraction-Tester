# tests_normalize.py
# ------------------------------------------------------------
# Hypothesis‑based test suite for the `normalize` function.
# ------------------------------------------------------------
# The function under test is expected to live in:
#   dataset/python_programs/normalize.py
# ------------------------------------------------------------

import math
from typing import List

import pytest
from hypothesis import given, assume, settings
from hypothesis import strategies as st

# Import the function under test.
# Adjust the import path if the module name or location differs.
from dataset.python_programs.normalize import normalize


# ----------------------------------------------------------------------
# Helper strategy: a list of numbers (int or float) with optional
# constraints on length and sum.
# ----------------------------------------------------------------------
def number_lists(
    min_size: int = 0,
    max_size: int = 10,
    allow_zero_sum: bool = True,
):
    """Generate a list of ints/floats satisfying the given constraints."""
    base = st.lists(
        st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False)),
        min_size=min_size,
        max_size=max_size,
    )

    # If we must avoid a zero sum (to prevent division‑by‑zero),
    # filter out those examples.
    if not allow_zero_sum:
        base = base.filter(lambda xs: not math.isclose(sum(xs), 0.0, abs_tol=1e-12))

    return base


# ----------------------------------------------------------------------
# 1. Property: preserves_length
#    Precondition: input is a list of numbers.
#    Formal: len(output) == len(input)
# ----------------------------------------------------------------------
@given(xs=number_lists())
@settings(max_examples=200)
def test_preserves_length(xs: List[float]) -> None:
    """The normalized list must have the same length as the input."""
    # Precondition is already satisfied by the strategy.
    output = normalize(xs)
    assert isinstance(output, list)
    assert len(output) == len(xs)


# ----------------------------------------------------------------------
# 2. Branch: len(xs) == 0  →  output == []
#    Precondition: len(xs) == 0
#    Formal: output == []
# ----------------------------------------------------------------------
@given(xs=number_lists(min_size=0, max_size=0))
def test_branch_empty(xs: List[float]) -> None:
    """When the input list is empty, the function should return an empty list."""
    output = normalize(xs)
    assert output == []


# ----------------------------------------------------------------------
# 3. Branch: len(xs) != 0  →  output == [x / sum(xs) for x in xs]
#    Precondition: len(xs) > 0
#    Formal: output == [x / sum(xs) for x in xs]
# ----------------------------------------------------------------------
@given(xs=number_lists(min_size=1, allow_zero_sum=False))
def test_branch_nonempty(xs: List[float]) -> None:
    """When the input list is non‑empty, the function should return the normalized values."""
    total = sum(xs)
    expected = [x / total for x in xs]
    output = normalize(xs)
    assert output == expected


# ----------------------------------------------------------------------
# 4. Return postcondition (empty input)
#    Precondition: len(xs) == 0
#    Formal: output == []
# ----------------------------------------------------------------------
@given(xs=number_lists(min_size=0, max_size=0))
def test_return_postcondition_empty(xs: List[float]) -> None:
    """Post‑condition for the empty‑input case."""
    output = normalize(xs)
    assert output == []


# ----------------------------------------------------------------------
# 5. Return postcondition (non‑empty input)
#    Precondition: len(xs) > 0
#    Formal: output == [x / sum(xs) for x in xs]
# ----------------------------------------------------------------------
@given(xs=number_lists(min_size=1, allow_zero_sum=False))
def test_return_postcondition_normalized(xs: List[float]) -> None:
    """Post‑condition for the non‑empty input case."""
    total = sum(xs)
    expected = [x / total for x in xs]
    output = normalize(xs)
    assert output == expected


# ----------------------------------------------------------------------
# 6. Loop invariant (trivial – no loop present)
#    Formal: True  # No loop present; invariant trivially holds
# ----------------------------------------------------------------------
@given(xs=number_lists())
def test_loop_invariant(xs: List[float]) -> None:
    """There is no loop in `normalize`; the invariant holds trivially."""
    # The test simply ensures the function runs without error.
    _ = normalize(xs)
    assert True  # Invariant satisfied by definition.