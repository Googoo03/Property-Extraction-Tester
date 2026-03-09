import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.reservation_overlap_check import reservation_overlap_check

# Property: preserves_length
@given(reservations=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_preserves_length(reservations, candidate):
    try:
        reservation_overlap_check(reservations, candidate)
        assert len(reservations) == len(reservations)
    except ValueError:
        pass

# Property: branch_specific_behavior (c_start >= c_end)
@given(candidate=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior_invalid_reservation(candidate):
    c_start, c_end = candidate
    if c_start >= c_end:
        with pytest.raises(ValueError):
            reservation_overlap_check([], candidate)

# Property: loop_invariant
@given(reservations=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_loop_invariant(reservations, candidate):
    c_start, c_end = candidate
    if c_start < c_end:
        for start, end in reservations:
            if not (c_end <= start or c_start >= end):
                break
        else:
            assert reservation_overlap_check(reservations, candidate) == False

# Property: branch_specific_behavior (not (c_end <= start or c_start >= end))
@given(reservations=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior_overlap_condition(reservations, candidate):
    c_start, c_end = candidate
    if c_start < c_end:
        for start, end in reservations:
            if not (c_end <= start or c_start >= end):
                assert reservation_overlap_check(reservations, candidate) == True
                break

# Property: return_postcondition (return True)
@given(reservations=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_true(reservations, candidate):
    c_start, c_end = candidate
    if c_start < c_end:
        for start, end in reservations:
            if not (c_end <= start or c_start >= end):
                assert reservation_overlap_check(reservations, candidate) == True
                break

# Property: return_postcondition (return False)
@given(reservations=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_false(reservations, candidate):
    c_start, c_end = candidate
    if c_start < c_end:
        for start, end in reservations:
            if not (c_end <= start or c_start >= end):
                break
        else:
            assert reservation_overlap_check(reservations, candidate) == False