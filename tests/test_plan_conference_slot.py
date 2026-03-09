import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.plan_conference_slot import plan_conference_slot

# Test for 'preserves_length' property of 'plan_conference_slot' function
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_plan_conference_slot_preserves_length(existing, candidate):
    output = plan_conference_slot(existing, candidate)
    assert len(output[1]) == len(existing) or len(output[1]) == len(existing) + 1

# Test for 'branch_specific_behavior' property of 'plan_conference_slot' function
@given(candidate=st.tuples(st.integers(), st.integers()))
def test_plan_conference_slot_branch_specific_behavior(candidate):
    if candidate[0] >= candidate[1]:
        with pytest.raises(ValueError):
            plan_conference_slot([], candidate)

# Test for 'preserves_length' property of 'overlaps' function
@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_overlaps_preserves_length(a, b):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    output = overlaps(a, b)
    assert output in [True, False]

# Test for 'return_postcondition' property of 'overlaps' function
@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_overlaps_return_postcondition(a, b):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    output = overlaps(a, b)
    assert output == (not (b[1] <= a[0] or b[0] >= a[1]))

# Test for 'loop_invariant' property of 'plan_conference_slot' function
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_plan_conference_slot_loop_invariant(existing, candidate):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    for i, slot in enumerate(existing):
        assert all(not overlaps(s, candidate) for s in existing[:i])

# Test for 'branch_specific_behavior' property of 'plan_conference_slot' function
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_plan_conference_slot_branch_specific_behavior(existing, candidate):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    for slot in existing:
        if overlaps(slot, candidate):
            output = plan_conference_slot(existing, candidate)
            assert output == (False, list(existing))

# Test for 'return_postcondition' property of 'plan_conference_slot' function
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_plan_conference_slot_return_postcondition(existing, candidate):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    for slot in existing:
        if overlaps(slot, candidate):
            output = plan_conference_slot(existing, candidate)
            assert output == (False, list(existing))
            break
    else:
        merged = list(existing) + [candidate]
        merged.sort()
        output = plan_conference_slot(existing, candidate)
        assert output == (True, merged)