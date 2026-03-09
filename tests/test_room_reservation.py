import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.room_reservation import room_reservation

# Test for preserves_length property
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_preserves_length(existing, interval):
    existing = sorted(existing)
    try:
        success, updated = room_reservation(existing, interval)
        assert len(updated) == len(existing) or len(updated) == len(existing) + 1
    except ValueError:
        pass

# Test for branch_specific_behavior when start >= end
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior_invalid_interval(existing, interval):
    start, end = interval
    if start >= end:
        with pytest.raises(ValueError, match="invalid interval"):
            room_reservation(existing, interval)

# Test for loop_invariant property
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_loop_invariant(existing, interval):
    existing = sorted(existing)
    start, end = interval
    for i, (s, e) in enumerate(existing):
        if not (end <= s or start >= e):
            success, updated = room_reservation(existing, interval)
            assert success == False
            assert updated == existing
            break

# Test for branch_specific_behavior when overlap exists
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior_overlap(existing, interval):
    existing = sorted(existing)
    start, end = interval
    for s, e in existing:
        if not (end <= s or start >= e):
            success, updated = room_reservation(existing, interval)
            assert success == False
            assert updated == existing
            return

# Test for return_postcondition when overlap exists
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_overlap(existing, interval):
    existing = sorted(existing)
    start, end = interval
    for s, e in existing:
        if not (end <= s or start >= e):
            success, updated = room_reservation(existing, interval)
            assert success == False
            assert updated == existing
            return

# Test for return_postcondition when no overlap
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_no_overlap(existing, interval):
    existing = sorted(existing)
    start, end = interval
    overlap = False
    for s, e in existing:
        if not (end <= s or start >= e):
            overlap = True
            break
    if not overlap:
        success, updated = room_reservation(existing, interval)
        assert success == True
        assert updated == sorted(existing + [interval])