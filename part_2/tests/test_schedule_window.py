import hypothesis
from hypothesis import given
import hypothesis.strategies as st
from dataset.python_programs.schedule_window import schedule_window

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_preserves_length(existing, interval):
    existing = sorted(existing)
    success, output = schedule_window(existing, interval)
    if success:
        assert len(output) == len(existing) + 1

@given(interval=st.tuples(st.integers(), st.integers()))
def test_invalid_interval_raises_value_error(interval):
    start, end = interval
    if start >= end:
        with hypothesis.raises(ValueError, match="invalid interval"):
            schedule_window([], interval)

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_loop_invariant(existing, interval):
    existing = sorted(existing)
    start, end = interval
    for s, e in existing:
        if not (end <= s or start >= e):
            success, output = schedule_window(existing, interval)
            assert not success
            assert output == existing
            return
    success, output = schedule_window(existing, interval)
    assert success
    assert output == sorted(existing + [interval])

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_branch_not_overlap(existing, interval):
    existing = sorted(existing)
    start, end = interval
    for s, e in existing:
        if not (end <= s or start >= e):
            success, output = schedule_window(existing, interval)
            assert not success
            assert output == existing
            return

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_false(existing, interval):
    existing = sorted(existing)
    start, end = interval
    for s, e in existing:
        if not (end <= s or start >= e):
            success, output = schedule_window(existing, interval)
            assert not success
            assert output == existing
            return

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), interval=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_true(existing, interval):
    existing = sorted(existing)
    start, end = interval
    for s, e in existing:
        if not (end <= s or start >= e):
            return
    success, output = schedule_window(existing, interval)
    assert success
    assert output == sorted(existing + [interval])