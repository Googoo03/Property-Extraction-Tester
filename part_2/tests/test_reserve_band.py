import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.reserve_band import reserve_band

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_reserve_band_preserves_length(existing, candidate):
    output, _ = reserve_band(existing, candidate)
    assert len(output) == len(existing) + (1 if candidate[0] < candidate[1] else 0)

@given(candidate=st.tuples(st.integers(), st.integers()))
def test_reserve_band_branch_specific_behavior(candidate):
    if candidate[0] >= candidate[1]:
        with pytest.raises(ValueError):
            reserve_band([], candidate)

@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_overlaps_preserves_length(a, b):
    # This test is not applicable as overlaps is a nested function and not directly accessible
    pass

@given(a=st.tuples(st.integers(), st.integers()), b=st.tuples(st.integers(), st.integers()))
def test_overlaps_return_postcondition(a, b):
    # This test is not applicable as overlaps is a nested function and not directly accessible
    pass

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_reserve_band_loop_invariant(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            assert slot[0] <= slot[1]
        _, output = reserve_band(existing, candidate)
        for slot in output:
            assert slot[0] <= slot[1]

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_reserve_band_branch_specific_behavior_overlap(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            if not (candidate[1] <= slot[0] or candidate[0] >= slot[1]):
                success, output = reserve_band(existing, candidate)
                assert not success
                assert output == existing
                return
        success, output = reserve_band(existing, candidate)
        assert success
        assert output == sorted(existing + [candidate])

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_reserve_band_return_postcondition_no_overlap(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            if not (candidate[1] <= slot[0] or candidate[0] >= slot[1]):
                return
        success, output = reserve_band(existing, candidate)
        assert success
        assert output == sorted(existing + [candidate])

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_reserve_band_return_postcondition_overlap(existing, candidate):
    if candidate[0] < candidate[1]:
        for slot in existing:
            if not (candidate[1] <= slot[0] or candidate[0] >= slot[1]):
                success, output = reserve_band(existing, candidate)
                assert not success
                assert output == existing
                return