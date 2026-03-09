import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.maintenance_booking import maintenance_booking

# Test for 'preserves_length' property
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_preserves_length(timeline, window):
    try:
        success, result = maintenance_booking(timeline, window)
        if success:
            assert len(result) == len(timeline) + 1
        else:
            assert len(result) == len(timeline)
    except ValueError:
        pass

# Test for 'branch_specific_behavior' when a >= b
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_branch_a_ge_b(timeline, window):
    a, b = window
    if a >= b:
        with pytest.raises(ValueError):
            maintenance_booking(timeline, window)

# Test for 'branch_specific_behavior' when any(not (b <= s or a >= e) for s, e in timeline)
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_branch_overlap(timeline, window):
    a, b = window
    if any(not (b <= s or a >= e) for s, e in timeline):
        success, result = maintenance_booking(timeline, window)
        assert not success
        assert result == timeline

# Test for 'return_postcondition' when return False, timeline
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_false(timeline, window):
    a, b = window
    if any(not (b <= s or a >= e) for s, e in timeline):
        success, result = maintenance_booking(timeline, window)
        assert not success
        assert result == timeline

# Test for 'return_postcondition' when return True, result
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_true(timeline, window):
    a, b = window
    if a < b and not any(not (b <= s or a >= e) for s, e in timeline):
        success, result = maintenance_booking(timeline, window)
        assert success
        assert result == sorted(timeline + [window])