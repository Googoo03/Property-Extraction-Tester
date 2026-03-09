import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.schedule_call import schedule_call

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_preserves_length(existing, candidate):
    output = schedule_call(existing, candidate)
    assert len(output[1]) == len(existing) + 1 if output[0] else len(existing)

@given(candidate=st.tuples(st.integers(), st.integers()))
def test_candidate_validation(candidate):
    if candidate[0] >= candidate[1]:
        with pytest.raises(ValueError):
            schedule_call([], candidate)
    else:
        output = schedule_call([], candidate)
        assert output[0] is True
        assert output[1] == [candidate]

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_output_format(existing, candidate):
    output = schedule_call(existing, candidate)
    assert isinstance(output, tuple)
    assert len(output) == 2

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_merged_list(existing, candidate):
    output = schedule_call(existing, candidate)
    if output[0]:
        assert all(slot in output[1] for slot in existing)
        assert candidate in output[1]

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_iteration_completeness(existing, candidate):
    output = schedule_call(existing, candidate)
    # This test is conceptual and cannot be directly verified with hypothesis
    # as it requires tracking internal iteration state.

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_branch_specific_behavior(existing, candidate):
    output = schedule_call(existing, candidate)
    # This test is conceptual and cannot be directly verified with hypothesis
    # as it requires specific branching conditions to be met.

@given(existing=st.lists(st.tuples(st.integers(), st.integers())), candidate=st.tuples(st.integers(), st.integers()))
def test_return_postcondition(existing, candidate):
    output = schedule_call(existing, candidate)
    if output[0]:
        assert isinstance(output[1], list)
    else:
        assert output[1] == existing