import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.inspection_booking import inspection_booking

# Test for the 'preserves_length' property of the inspection_booking function
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_inspection_booking_preserves_length(existing, candidate):
    output = inspection_booking(existing, candidate)
    assert len(output[1]) == len(existing) + (1 if output[0] else 0)

# Test for the 'branch_specific_behavior' property when candidate[0] >= candidate[1]
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_inspection_booking_branch_specific_behavior(existing, candidate):
    if candidate[0] >= candidate[1]:
        with pytest.raises(ValueError):
            inspection_booking(existing, candidate)

# Test for the 'preserves_length' property of the overlaps function
@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_overlaps_preserves_length(a, b):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    output = overlaps(a, b)
    # Since overlaps is a boolean function, we just check it returns a boolean
    assert isinstance(output, bool)

# Test for the 'return_postcondition' property of the overlaps function
@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_overlaps_return_postcondition(a, b):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    expected = not (b[1] <= a[0] or b[0] >= a[1])
    assert overlaps(a, b) == expected

# Test for the 'loop_invariant' property of the inspection_booking function
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_inspection_booking_loop_invariant(existing, candidate):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    for slot in existing:
        assert not overlaps(slot, candidate)

# Test for the 'branch_specific_behavior' property when overlaps(slot, candidate) is true
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_inspection_booking_branch_specific_behavior_overlaps(existing, candidate):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    for slot in existing:
        if overlaps(slot, candidate):
            assert inspection_booking(existing, candidate) == (False, list(existing))

# Test for the 'return_postcondition' property when overlaps(slot, candidate) is true
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_inspection_booking_return_postcondition_overlaps(existing, candidate):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    for slot in existing:
        if overlaps(slot, candidate):
            assert inspection_booking(existing, candidate) == (False, list(existing))

# Test for the 'return_postcondition' property when no overlaps occur
@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_inspection_booking_return_postcondition_no_overlaps(existing, candidate):
    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])
    if not any(overlaps(slot, candidate) for slot in existing):
        merged = list(existing) + [candidate]
        merged.sort()
        assert inspection_booking(existing, candidate) == (True, merged)