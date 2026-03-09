import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.schedule_pickup import schedule_pickup

@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_preserves_length(timeline, window):
    a, b = window
    if a < b:
        _, result = schedule_pickup(timeline, window)
        assert len(result) == len(timeline) + 1

@given(window=st.tuples(st.integers(), st.integers()))
def test_branch_a_ge_b(window):
    a, b = window
    if a >= b:
        success, timeline = schedule_pickup([], window)
        assert not success
        assert timeline == []

@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_branch_any_overlap(timeline, window):
    a, b = window
    if a < b and any(not (b <= s or a >= e) for s, e in timeline):
        success, result = schedule_pickup(timeline, window)
        assert not success
        assert result == timeline

@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_false(timeline, window):
    a, b = window
    if a < b and any(not (b <= s or a >= e) for s, e in timeline):
        success, result = schedule_pickup(timeline, window)
        assert not success
        assert result == timeline

@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_true(timeline, window):
    a, b = window
    if a < b and not any(not (b <= s or a >= e) for s, e in timeline):
        success, result = schedule_pickup(timeline, window)
        assert success
        assert result == sorted(timeline + [window])