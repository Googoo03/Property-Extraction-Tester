import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.plan_appointment_slot import plan_appointment_slot

# Test for 'preserves_length' property
@given(
    timeline=st.lists(st.tuples(st.integers(), st.integers())),
    window=st.tuples(st.integers(), st.integers())
)
def test_preserves_length(timeline, window):
    a, b = window
    try:
        success, result = plan_appointment_slot(timeline, window)
        if success:
            assert len(result) == len(timeline) + 1
        else:
            assert len(result) == len(timeline)
    except ValueError:
        pass

# Test for 'branch_specific_behavior' when a >= b
@given(
    timeline=st.lists(st.tuples(st.integers(), st.integers())),
    window=st.tuples(st.integers(), st.integers())
)
def test_branch_a_ge_b(timeline, window):
    a, b = window
    if a >= b:
        with pytest.raises(ValueError):
            plan_appointment_slot(timeline, window)

# Test for 'branch_specific_behavior' when any(not (b <= s or a >= e) for s, e in timeline)
@given(
    timeline=st.lists(st.tuples(st.integers(), st.integers())),
    window=st.tuples(st.integers(), st.integers())
)
def test_branch_any_overlap(timeline, window):
    a, b = window
    if a < b and any(not (b <= s or a >= e) for s, e in timeline):
        success, result = plan_appointment_slot(timeline, window)
        assert not success
        assert result == timeline

# Test for 'return_postcondition' when return False, timeline
@given(
    timeline=st.lists(st.tuples(st.integers(), st.integers())),
    window=st.tuples(st.integers(), st.integers())
)
def test_return_false_timeline(timeline, window):
    a, b = window
    if a < b and any(not (b <= s or a >= e) for s, e in timeline):
        success, result = plan_appointment_slot(timeline, window)
        assert not success
        assert result == timeline

# Test for 'return_postcondition' when return True, result
@given(
    timeline=st.lists(st.tuples(st.integers(), st.integers())),
    window=st.tuples(st.integers(), st.integers())
)
def test_return_true_result(timeline, window):
    a, b = window
    if a < b and not any(not (b <= s or a >= e) for s, e in timeline):
        success, result = plan_appointment_slot(timeline, window)
        assert success
        assert result == sorted(timeline + [window])