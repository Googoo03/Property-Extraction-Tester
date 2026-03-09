import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.plan_upgrade_slot import plan_upgrade_slot

# Test for property: preserves_length
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_preserves_length(timeline, window):
    try:
        success, result = plan_upgrade_slot(timeline, window)
        if success:
            assert len(result) == len(timeline) + 1
        else:
            assert len(result) == len(timeline)
    except ValueError:
        pass

# Test for branch-specific behavior: a >= b
@given(window=st.tuples(st.integers(), st.integers()))
def test_branch_a_ge_b(window):
    a, b = window
    timeline = []
    if a >= b:
        with hypothesis.assume(True):
            try:
                success, result = plan_upgrade_slot(timeline, window)
                assert False, "Expected ValueError"
            except ValueError:
                pass

# Test for branch-specific behavior: any(not (b <= s or a >= e) for s, e in timeline)
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_branch_any_condition(timeline, window):
    a, b = window
    if timeline and any(not (b <= s or a >= e) for s, e in timeline):
        with hypothesis.assume(True):
            success, result = plan_upgrade_slot(timeline, window)
            assert not success
            assert result == timeline

# Test for return postcondition: return False, timeline
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_false_timeline(timeline, window):
    a, b = window
    if timeline and any(not (b <= s or a >= e) for s, e in timeline):
        with hypothesis.assume(True):
            success, result = plan_upgrade_slot(timeline, window)
            assert not success
            assert result == timeline

# Test for return postcondition: return True, result
@given(timeline=st.lists(st.tuples(st.integers(), st.integers())), window=st.tuples(st.integers(), st.integers()))
def test_return_true_result(timeline, window):
    a, b = window
    if not (a >= b) and (not timeline or all(b <= s or a >= e for s, e in timeline)):
        with hypothesis.assume(True):
            success, result = plan_upgrade_slot(timeline, window)
            assert success
            assert result == sorted(timeline + [window])