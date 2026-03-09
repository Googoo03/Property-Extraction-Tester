import pytest
from hypothesis import given
from hypothesis.strategies import lists, tuples, integers
from dataset.python_programs.machine_booking import machine_booking

@given(timeline=lists(tuples(integers(), integers())), window=tuples(integers(), integers()))
def test_preserves_length(timeline, window):
    a, b = window
    if a < b:
        success, result = machine_booking(timeline, window)
        if success:
            assert len(result) == len(timeline) + 1

@given(timeline=lists(tuples(integers(), integers())), window=tuples(integers(), integers()))
def test_branch_a_ge_b(timeline, window):
    a, b = window
    if a >= b:
        success, result = machine_booking(timeline, window)
        assert not success
        assert result == timeline

@given(timeline=lists(tuples(integers(), integers())), window=tuples(integers(), integers()))
def test_branch_any_overlap(timeline, window):
    a, b = window
    if a < b:
        overlap = any(not (b <= s or a >= e) for s, e in timeline)
        success, result = machine_booking(timeline, window)
        if overlap:
            assert not success
            assert result == timeline
        else:
            assert success
            assert result == sorted(timeline + [window])

@given(timeline=lists(tuples(integers(), integers())), window=tuples(integers(), integers()))
def test_return_postcondition_false(timeline, window):
    a, b = window
    if a < b:
        overlap = any(not (b <= s or a >= e) for s, e in timeline)
        if overlap:
            success, result = machine_booking(timeline, window)
            assert not success
            assert result == timeline

@given(timeline=lists(tuples(integers(), integers())), window=tuples(integers(), integers()))
def test_return_postcondition_true(timeline, window):
    a, b = window
    if a < b:
        overlap = any(not (b <= s or a >= e) for s, e in timeline)
        if not overlap:
            success, result = machine_booking(timeline, window)
            assert success
            assert result == sorted(timeline + [window])