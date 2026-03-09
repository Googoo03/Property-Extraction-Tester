import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.downtime_booking import downtime_booking

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuple(st.integers(), st.integers()))
def test_downtime_booking_preserves_length(existing, candidate):
    try:
        output = downtime_booking(existing, candidate)
        assert len(output[1]) == len(existing) or len(output[1]) == len(existing) + 1
    except ValueError:
        pass

@given(candidate=st.tuple(st.integers(), st.integers()))
def test_downtime_booking_branch_specific_behavior(candidate):
    if candidate[0] >= candidate[1]:
        with pytest.raises(ValueError):
            downtime_booking([], candidate)

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuple(st.integers(), st.integers()))
def test_downtime_booking_loop_invariant(existing, candidate):
    try:
        output = downtime_booking(existing, candidate)
        if candidate[0] < candidate[1]:
            assert len(output[1]) == len(existing) or len(output[1]) == len(existing) + 1
    except ValueError:
        pass

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuple(st.integers(), st.integers()))
def test_downtime_booking_branch_specific_behavior_overlap(existing, candidate):
    try:
        output = downtime_booking(existing, candidate)
        if candidate[0] < candidate[1]:
            if any(not (candidate[1] <= slot[0] or candidate[0] >= slot[1]) for slot in existing):
                assert output[0] is False
            else:
                assert output[0] is True
    except ValueError:
        pass

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuple(st.integers(), st.integers()))
def test_downtime_booking_return_postcondition_false(existing, candidate):
    try:
        output = downtime_booking(existing, candidate)
        if candidate[0] < candidate[1]:
            if any(not (candidate[1] <= slot[0] or candidate[0] >= slot[1]) for slot in existing):
                assert output == (False, existing)
    except ValueError:
        pass

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuple(st.integers(), st.integers()))
def test_downtime_booking_return_postcondition_true(existing, candidate):
    try:
        output = downtime_booking(existing, candidate)
        if candidate[0] < candidate[1]:
            if not any(not (candidate[1] <= slot[0] or candidate[0] >= slot[1]) for slot in existing):
                merged = sorted(existing + [candidate])
                assert output == (True, merged)
    except ValueError:
        pass