import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.schedule_demo import schedule_demo

# Test property: preserves_length
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10),
    interval=st.tuples(st.integers(), st.integers())
)
def test_preserves_length(existing, interval):
    existing_sorted = sorted(existing)
    success, output = schedule_demo(existing_sorted, interval)
    if success:
        assert len(output) == len(existing_sorted) + 1
    else:
        assert len(output) == len(existing_sorted)

# Test property: branch_specific_behavior (raises ValueError if start >= end)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10),
    interval=st.tuples(st.integers(), st.integers()).filter(lambda x: x[0] >= x[1])
)
def test_raises_value_error_on_invalid_interval(existing, interval):
    existing_sorted = sorted(existing)
    with pytest.raises(ValueError):
        schedule_demo(existing_sorted, interval)

# Test property: loop_invariant (loop checks all existing intervals for overlap)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10),
    interval=st.tuples(st.integers(), st.integers())
)
def test_loop_invariant(existing, interval):
    existing_sorted = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing_sorted:
            if not (end <= s or start >= e):
                success, _ = schedule_demo(existing_sorted, interval)
                assert not success
                return
        success, _ = schedule_demo(existing_sorted, interval)
        assert success

# Test property: branch_specific_behavior (returns False, existing if overlap detected)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=1, max_size=10),
    interval=st.tuples(st.integers(), st.integers())
)
def test_returns_false_if_overlap_detected(existing, interval):
    existing_sorted = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing_sorted:
            if not (end <= s or start >= e):
                success, output = schedule_demo(existing_sorted, interval)
                assert not success
                assert output == existing_sorted
                return

# Test property: return_postcondition (returns value satisfying expected semantics: return False, existing if overlap detected)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=1, max_size=10),
    interval=st.tuples(st.integers(), st.integers())
)
def test_return_postcondition_false_on_overlap(existing, interval):
    existing_sorted = sorted(existing)
    start, end = interval
    if start < end:
        for s, e in existing_sorted:
            if not (end <= s or start >= e):
                success, output = schedule_demo(existing_sorted, interval)
                assert not success
                assert output == existing_sorted

# Test property: return_postcondition (returns value satisfying expected semantics: return True, updated if no overlap)
@given(
    existing=st.lists(st.tuples(st.integers(), st.integers()), min_size=0, max_size=10),
    interval=st.tuples(st.integers(), st.integers())
)
def test_return_postcondition_true_if_no_overlap(existing, interval):
    existing_sorted = sorted(existing)
    start, end = interval
    if start < end:
        overlap = any(not (end <= s or start >= e) for s, e in existing_sorted)
        success, output = schedule_demo(existing_sorted, interval)
        if not overlap:
            assert success
            assert output == sorted(existing_sorted + [interval])
        else:
            assert not success
            assert output == existing_sorted