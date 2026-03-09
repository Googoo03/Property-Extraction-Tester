import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.reservation_booking import reservation_booking

# Helper function to check if two intervals overlap
def intervals_overlap(a, b):
    return not (a[1] <= b[0] or a[0] >= b[1])

# Property: preserves_length
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10).map(
        lambda lst: sorted(lst, key=lambda x: x[0])
    ),
    interval=st.tuples(st.integers(), st.integers())
)
def test_preserves_length(existing, interval):
    start, end = interval
    if start >= end:
        with pytest.raises(ValueError):
            reservation_booking(existing, interval)
    else:
        overlap_exists = any(intervals_overlap(interval, e) for e in existing)
        success, updated = reservation_booking(existing, interval)
        if overlap_exists:
            assert len(updated) == len(existing)
        else:
            assert len(updated) == len(existing) + 1

# Property: branch_specific_behavior (start >= end)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10).map(
        lambda lst: sorted(lst, key=lambda x: x[0])
    ),
    interval=st.tuples(st.integers(), st.integers())
)
def test_branch_start_end(existing, interval):
    start, end = interval
    if start >= end:
        with pytest.raises(ValueError):
            reservation_booking(existing, interval)

# Property: loop_invariant
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10).map(
        lambda lst: sorted(lst, key=lambda x: x[0])
    ),
    interval=st.tuples(st.integers(), st.integers())
)
def test_loop_invariant(existing, interval):
    start, end = interval
    if start < end:
        no_overlap_holds = True
        for i, (s, e) in enumerate(existing):
            if not (end <= s or start >= e):
                no_overlap_holds = False
                break
            # Check invariant: no overlap with previous intervals
            assert all(end <= prev_s or start >= prev_e for prev_s, prev_e in existing[:i])
        success, updated = reservation_booking(existing, interval)
        if no_overlap_holds:
            assert success
        else:
            assert not success

# Property: branch_specific_behavior (overlap detected)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10).map(
        lambda lst: sorted(lst, key=lambda x: x[0])
    ),
    interval=st.tuples(st.integers(), st.integers())
)
def test_branch_overlap_detected(existing, interval):
    start, end = interval
    if start < end:
        success, updated = reservation_booking(existing, interval)
        overlap_exists = any(intervals_overlap(interval, e) for e in existing)
        if overlap_exists:
            assert not success
            assert updated == existing

# Property: return_postcondition (overlap exists)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10).map(
        lambda lst: sorted(lst, key=lambda x: x[0])
    ),
    interval=st.tuples(st.integers(), st.integers())
)
def test_return_overlap_exists(existing, interval):
    start, end = interval
    if start < end:
        overlap_exists = any(intervals_overlap(interval, e) for e in existing)
        success, updated = reservation_booking(existing, interval)
        if overlap_exists:
            assert not success
            assert updated == existing

# Property: return_postcondition (no overlap)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10).map(
        lambda lst: sorted(lst, key=lambda x: x[0])
    ),
    interval=st.tuples(st.integers(), st.integers())
)
def test_return_no_overlap(existing, interval):
    start, end = interval
    if start < end:
        overlap_exists = any(intervals_overlap(interval, e) for e in existing)
        success, updated = reservation_booking(existing, interval)
        if not overlap_exists:
            assert success
            assert updated == sorted(existing + [interval])