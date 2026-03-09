import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.reserve_lane import reserve_lane

@given(candidate=st.tuples(st.integers(), st.integers()))
def test_input_validation(candidate):
    if candidate[0] < candidate[1]:
        reserve_lane([], candidate)
    else:
        with pytest.raises(ValueError):
            reserve_lane([], candidate)

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_preserves_existing(existing, candidate):
    if candidate[0] < candidate[1]:
        success, output = reserve_lane(existing, candidate)
        assert output == existing or output == sorted(existing + [candidate])

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_raises_error(existing, candidate):
    if candidate[0] >= candidate[1]:
        with pytest.raises(ValueError):
            reserve_lane(existing, candidate)

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_returns_existing(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            if slot[0] < candidate[1] and candidate[0] < slot[1]:
                success, output = reserve_lane(existing, candidate)
                assert (success, output) == (False, list(existing))
                break

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_continues_loop(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            if not (slot[1] <= candidate[0] or candidate[1] <= slot[0]):
                break
        else:
            success, output = reserve_lane(existing, candidate)
            assert success is True

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_return_success(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            if slot[0] < candidate[1] and candidate[0] < slot[1]:
                break
        else:
            success, output = reserve_lane(existing, candidate)
            assert (success, output) == (True, sorted(existing + [candidate]))

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_return_failure(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            if slot[0] < candidate[1] and candidate[0] < slot[1]:
                success, output = reserve_lane(existing, candidate)
                assert (success, output) == (False, list(existing))
                break

@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_boundary_touch(a, b):
    if a[1] == b[0] or b[1] == a[0]:
        assert reserve_lane.overlaps(a, b) is True

@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_no_overlap(a, b):
    if a[1] <= b[0] or b[1] <= a[0]:
        assert reserve_lane.overlaps(a, b) is False

@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_full_overlap(a, b):
    if a[0] < b[0] < b[1] < a[1] or b[0] < a[0] < a[1] < b[1]:
        assert reserve_lane.overlaps(a, b) is True

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_iterates_all(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            if slot[0] < candidate[1] and candidate[0] < slot[1]:
                break
        else:
            success, output = reserve_lane(existing, candidate)
            assert success is True

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_no_side_effects(existing, candidate):
    if candidate[0] < candidate[1]:
        existing_copy = list(existing)
        reserve_lane(existing, candidate)
        assert existing == existing_copy

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_output_type(existing, candidate):
    if candidate[0] < candidate[1]:
        success, output = reserve_lane(existing, candidate)
        assert isinstance(success, bool)
        assert isinstance(output, list)
        assert len(output) == len(existing) + (1 if success else 0)

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_merged_sorted(existing, candidate):
    if candidate[0] < candidate[1]:
        success, output = reserve_lane(existing, candidate)
        assert output == sorted(output)