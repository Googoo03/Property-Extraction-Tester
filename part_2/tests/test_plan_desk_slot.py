import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.plan_desk_slot import plan_desk_slot

# Property: preserves_length
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_preserves_length(existing, interval):
    existing = sorted(existing)
    success, output = plan_desk_slot(existing, interval)
    if success:
        assert len(output) == len(existing) + 1
    else:
        assert len(output) == len(existing)

# Property: branch_specific_behavior (start >= end)
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_branch_start_end_condition(existing, interval):
    start, end = interval
    if start >= end:
        with pytest.raises(ValueError):
            plan_desk_slot(existing, interval)
    else:
        result = plan_desk_slot(existing, interval)
        assert isinstance(result, tuple)

# Property: loop_invariant
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_loop_invariant(existing, interval):
    existing = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing:
            if not (end <= s or start >= e):
                success, _ = plan_desk_slot(existing, interval)
                assert not success
                return
        success, updated = plan_desk_slot(existing, interval)
        assert success
        assert updated == sorted(existing + [interval])

# Property: branch_specific_behavior (overlap condition)
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_branch_overlap_condition(existing, interval):
    existing = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing:
            if not (end <= s or start >= e):
                success, _ = plan_desk_slot(existing, interval)
                assert not success
                return
        success, _ = plan_desk_slot(existing, interval)
        assert success

# Property: return_postcondition (return False, existing)
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_return_false(existing, interval):
    existing = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing:
            if not (end <= s or start >= e):
                success, output = plan_desk_slot(existing, interval)
                assert not success
                assert output == existing
                return

# Property: return_postcondition (return True, updated)
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_return_true(existing, interval):
    existing = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing:
            if not (end <= s or start >= e):
                return
        success, output = plan_desk_slot(existing, interval)
        assert success
        assert output == sorted(existing + [interval])