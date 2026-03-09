import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.schedule_training import schedule_training

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_preserves_length(existing, interval):
    existing_sorted = sorted(existing)
    try:
        success, updated = schedule_training(existing_sorted, interval)
        if success:
            assert len(updated) == len(existing_sorted) + 1
    except ValueError:
        pass

@given(interval=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior(interval):
    start, end = interval
    existing = []
    if start >= end:
        with pytest.raises(ValueError):
            schedule_training(existing, interval)
    else:
        success, _ = schedule_training(existing, interval)
        assert isinstance(success, bool)

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_loop_invariant(existing, interval):
    existing_sorted = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing_sorted:
            if not (end <= s or start >= e):
                success, _ = schedule_training(existing_sorted, interval)
                assert not success
                return
        success, _ = schedule_training(existing_sorted, interval)
        assert success

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior_overlap(existing, interval):
    existing_sorted = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing_sorted:
            if not (end <= s or start >= e):
                success, updated = schedule_training(existing_sorted, interval)
                assert not success
                assert updated == existing_sorted
                return

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_false(existing, interval):
    existing_sorted = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing_sorted:
            if not (end <= s or start >= e):
                success, updated = schedule_training(existing_sorted, interval)
                assert not success
                assert updated == existing_sorted

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_true(existing, interval):
    existing_sorted = sorted(existing)
    start, end = interval
    if start < end:
        overlap = False
        for s, e in existing_sorted:
            if not (end <= s or start >= e):
                overlap = True
                break
        if not overlap:
            success, updated = schedule_training(existing_sorted, interval)
            assert success
            assert updated == sorted(existing_sorted + [interval])