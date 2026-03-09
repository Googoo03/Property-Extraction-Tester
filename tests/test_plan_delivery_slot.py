import hypothesis
from hypothesis import given, strategies as st
import pytest

from dataset.python_programs.plan_delivery_slot import plan_delivery_slot

# Property: preserves_length
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_preserves_length(timeline, window):
    a, b = window
    if a >= b:
        output = plan_delivery_slot(timeline, window)
        assert len(output[1]) == len(timeline)
    else:
        output = plan_delivery_slot(timeline, window)
        if output[0]:
            assert len(output[1]) == len(timeline) + 1
        else:
            assert len(output[1]) == len(timeline)

# Property: branch_specific_behavior (a >= b)
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior_a_greater_equal_b(timeline, window):
    a, b = window
    if a >= b:
        output = plan_delivery_slot(timeline, window)
        assert output == (False, timeline)

# Property: branch_specific_behavior (any(not (b <= s or a >= e) for s, e in timeline))
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior_conflict(timeline, window):
    a, b = window
    if a < b and any(not (b <= s or a >= e) for s, e in timeline):
        output = plan_delivery_slot(timeline, window)
        assert output == (False, timeline)

# Property: return_postcondition (output[0] == False and output[1] == timeline)
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_false(timeline, window):
    a, b = window
    if a >= b or (a < b and any(not (b <= s or a >= e) for s, e in timeline)):
        output = plan_delivery_slot(timeline, window)
        assert output[0] == False and output[1] == timeline

# Property: return_postcondition (output[0] == True and output[1] == sorted(timeline + [window]))
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_postcondition_true(timeline, window):
    a, b = window
    if a < b and not any(not (b <= s or a >= e) for s, e in timeline):
        output = plan_delivery_slot(timeline, window)
        assert output[0] == True and output[1] == sorted(timeline + [window])