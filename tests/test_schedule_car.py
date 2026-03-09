import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.schedule_car import schedule_car

# Property: preserves_length
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_preserves_length(timeline, window):
    output, _ = schedule_car(timeline, window)
    if output:
        assert len(timeline) + 1 == len(schedule_car(timeline, window)[1])
    else:
        assert len(timeline) == len(schedule_car(timeline, window)[1])

# Property: branch_specific_behavior for a >= b
@given(window=st.tuples(st.integers(), st.integers()))
def test_branch_a_ge_b(window):
    a, b = window
    timeline = []
    if a >= b:
        with pytest.raises(ValueError):
            schedule_car(timeline, window)

# Property: branch_specific_behavior for any(not (b <= s or a >= e) for s, e in timeline)
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_branch_overlap(timeline, window):
    a, b = window
    timeline = [(s, e) for s, e in timeline if not (b <= s or a >= e)]
    if timeline:
        output, _ = schedule_car(timeline, window)
        assert not output

# Property: return_postcondition for return False, timeline
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_false(timeline, window):
    a, b = window
    timeline = [(s, e) for s, e in timeline if not (b <= s or a >= e)]
    if timeline:
        output, result = schedule_car(timeline, window)
        assert not output
        assert result == timeline

# Property: return_postcondition for return True, result
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_true(timeline, window):
    a, b = window
    if a < b and not any(not (b <= s or a >= e) for s, e in timeline):
        output, result = schedule_car(timeline, window)
        assert output
        assert result == sorted(timeline + [window])