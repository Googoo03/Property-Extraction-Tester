import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.job_queue_priority import job_queue_priority

@given(jobs=st.lists(st.integers()))
def test_preserves_length(jobs):
    result = job_queue_priority(jobs)
    assert len(jobs) == len(jobs)

@given(max_jobs=st.integers().filter(lambda x: x < 0))
def test_branch_specific_behavior_raises_value_error(max_jobs):
    with pytest.raises(ValueError, match="max_jobs must be non-negative"):
        job_queue_priority([], max_jobs=max_jobs)

@given(jobs=st.lists(st.integers()), max_jobs=st.integers().filter(lambda x: x >= 0))
def test_branch_specific_behavior_returns_false(jobs, max_jobs):
    if len(jobs) > max_jobs:
        assert job_queue_priority(jobs, max_jobs=max_jobs) == False

@given(jobs=st.lists(st.integers()), max_jobs=st.integers().filter(lambda x: x >= 0))
def test_return_postcondition_returns_false_when_len_jobs_greater_than_max_jobs(jobs, max_jobs):
    if len(jobs) > max_jobs:
        assert job_queue_priority(jobs, max_jobs=max_jobs) == False

@given(jobs=st.lists(st.integers()), max_jobs=st.integers().filter(lambda x: x >= 0))
def test_return_postcondition_returns_true_when_len_jobs_less_than_or_equal_to_max_jobs(jobs, max_jobs):
    if len(jobs) <= max_jobs:
        assert job_queue_priority(jobs, max_jobs=max_jobs) == True