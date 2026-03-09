import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.batch_tally import batch_tally

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.integers().filter(lambda x: x >= 0) | st.none()
)
def test_preserves_length(counts, key, max_value):
    counts_copy = counts.copy()
    batch_tally(counts, key, max_value=max_value)
    assert len(counts) == len(counts_copy)

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.integers().filter(lambda x: x >= 0)
)
def test_branch_specific_behavior_max_value_not_none(counts, key, max_value):
    counts_copy = counts.copy()
    result = batch_tally(counts, key, max_value=max_value)
    if counts_copy.get(key, 0) + 1 > max_value:
        assert result == max_value
    else:
        assert result == counts_copy.get(key, 0) + 1

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.integers().filter(lambda x: x >= 0)
)
def test_branch_specific_behavior_new_value_exceeds_max(counts, key, max_value):
    counts_copy = counts.copy()
    result = batch_tally(counts, key, max_value=max_value)
    if counts_copy.get(key, 0) + 1 > max_value:
        assert counts[key] == max_value
    else:
        assert counts[key] == counts_copy.get(key, 0) + 1

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.integers().filter(lambda x: x >= 0) | st.none()
)
def test_return_postcondition(counts, key, max_value):
    result = batch_tally(counts, key, max_value=max_value)
    expected = counts.get(key, 0) + 1
    if max_value is not None and expected > max_value:
        expected = max_value
    assert result == expected