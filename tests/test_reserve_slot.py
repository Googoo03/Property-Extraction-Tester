import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.reserve_slot import reserve_slot

@given(candidate=st.tuples(st.floats(), st.floats()))
def test_input_validation(candidate):
    if candidate[0] < candidate[1]:
        try:
            reserve_slot([], candidate)
            assert True
        except ValueError:
            assert False
    else:
        with pytest.raises(ValueError):
            reserve_slot([], candidate)

@given(existing=st.lists(st.tuples(st.floats(), st.floats())), candidate=st.tuples(st.floats(), st.floats()))
def test_output_format(existing, candidate):
    if candidate[0] < candidate[1]:
        output = reserve_slot(existing, candidate)
        assert isinstance(output, tuple)
        assert len(output) == 2
        assert isinstance(output[0], bool)
        assert isinstance(output[1], list)

@given(existing=st.lists(st.tuples(st.floats(), st.floats())), candidate=st.tuples(st.floats(), st.floats()))
def test_output_slots_valid(existing, candidate):
    if candidate[0] < candidate[1]:
        output = reserve_slot(existing, candidate)
        assert all(slot[0] < slot[1] for slot in output[1])

@given(candidate=st.tuples(st.floats(), st.floats()))
def test_raises_exception(candidate):
    if candidate[0] >= candidate[1]:
        with pytest.raises(ValueError):
            reserve_slot([], candidate)

@given(existing=st.lists(st.tuples(st.floats(), st.floats())), candidate=st.tuples(st.floats(), st.floats()))
def test_returns_false(existing, candidate):
    if candidate[0] < candidate[1]:
        # Mock overlaps to always return True
        original_overlaps = reserve_slot.__globals__['overlaps']
        reserve_slot.__globals__['overlaps'] = lambda a, b: True
        output = reserve_slot(existing, candidate)
        assert output == (False, list(existing))
        reserve_slot.__globals__['overlaps'] = original_overlaps

@given(existing=st.lists(st.tuples(st.floats(), st.floats())), candidate=st.tuples(st.floats(), st.floats()))
def test_return_non_overlapping(existing, candidate):
    if candidate[0] < candidate[1]:
        output = reserve_slot(existing, candidate)
        if output[0]:
            assert all(not reserve_slot.__globals__['overlaps'](slot, candidate) for slot in existing)

@given()
def test_boundary_touch():
    assert reserve_slot.__globals__['overlaps']((1, 2), (2, 3)) == True

@given()
def test_proper_overlap():
    assert reserve_slot.__globals__['overlaps']((1, 3), (2, 4)) == True

@given()
def test_no_overlap():
    assert reserve_slot.__globals__['overlaps']((1, 2), (3, 4)) == False

@given()
def test_swapped_args():
    assert reserve_slot.__globals__['overlaps']((2, 4), (1, 3)) == True

@given()
def test_identical_slots():
    assert reserve_slot.__globals__['overlaps']((1, 3), (1, 3)) == True

@given(existing=st.lists(st.tuples(st.floats(), st.floats())), candidate=st.tuples(st.floats(), st.floats()))
def test_no_side_effects(existing, candidate):
    if candidate[0] < candidate[1]:
        original_existing = list(existing)
        reserve_slot(existing, candidate)
        assert existing == original_existing

@given(existing=st.lists(st.tuples(st.floats(), st.floats())), candidate=st.tuples(st.floats(), st.floats()))
def test_preserves_existing(existing, candidate):
    if candidate[0] < candidate[1]:
        output = reserve_slot(existing, candidate)
        assert all(slot in output[1] for slot in existing)

@given(existing=st.lists(st.tuples(st.floats(), st.floats())), candidate=st.tuples(st.floats(), st.floats()))
def test_adds_candidate_if_valid(existing, candidate):
    if candidate[0] < candidate[1]:
        output = reserve_slot(existing, candidate)
        if output[0]:
            assert candidate in output[1]