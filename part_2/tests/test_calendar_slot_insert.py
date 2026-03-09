import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from dataset.python_programs.calendar_slot_insert import calendar_slot_insert

# Generate time slots as tuples of integers (start, end)
time_slots = st.tuples(st.integers(), st.integers()).map(lambda x: (min(x), max(x)))

@given(existing=st.lists(time_slots), slot=time_slots)
def test_preserves_length(existing, slot):
    start, end = slot
    if start >= end:
        with pytest.raises(ValueError):
            calendar_slot_insert(existing, slot)
    else:
        success, output = calendar_slot_insert(existing, slot)
        if success:
            assert len(output) == len(existing) + 1
        else:
            assert len(output) == len(existing)

@given(slot=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior_invalid_slot(slot):
    start, end = slot
    if start >= end:
        with pytest.raises(ValueError):
            calendar_slot_insert([], slot)

@given(existing=st.lists(time_slots), slot=time_slots)
def test_loop_invariant(existing, slot):
    start, end = slot
    if start < end:
        for s, e in existing:
            if not (end <= s or start >= e):
                success, output = calendar_slot_insert(existing, slot)
                assert not success
                assert output == existing
                return
        success, output = calendar_slot_insert(existing, slot)
        assert success
        assert len(output) == len(existing) + 1

@given(existing=st.lists(time_slots), slot=time_slots)
def test_branch_specific_behavior_overlap(existing, slot):
    start, end = slot
    if start < end:
        for s, e in existing:
            if not (end <= s or start >= e):
                success, output = calendar_slot_insert(existing, slot)
                assert not success
                assert output == existing

@given(existing=st.lists(time_slots), slot=time_slots)
def test_return_postcondition_false(existing, slot):
    start, end = slot
    if start < end:
        for s, e in existing:
            if not (end <= s or start >= e):
                success, output = calendar_slot_insert(existing, slot)
                assert not success
                assert output == existing

@given(existing=st.lists(time_slots), slot=time_slots)
def test_return_postcondition_true(existing, slot):
    start, end = slot
    if start < end:
        overlapping = any(not (end <= s or start >= e) for s, e in existing)
        if not overlapping:
            success, output = calendar_slot_insert(existing, slot)
            assert success
            assert len(output) == len(existing) + 1
            assert slot in output