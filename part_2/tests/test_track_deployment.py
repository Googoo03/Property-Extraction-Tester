import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.track_deployment import track_deployment

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_preserve_length(counts, key, max_value):
    output = track_deployment(counts, key, max_value=max_value)
    assert len(output) == len(counts)

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_branch_specific_behavior_max_value_not_none(counts, key, max_value):
    if max_value is not None:
        track_deployment(counts, key, max_value=max_value)

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_branch_specific_behavior_new_value_greater_than_max_value(counts, key, max_value):
    if max_value is not None:
        track_deployment(counts, key, max_value=max_value)

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_return_postcondition(counts, key, max_value):
    output = track_deployment(counts, key, max_value=max_value)
    assert output == counts[key]

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_key_existence(counts, key, max_value):
    track_deployment(counts, key, max_value=max_value)
    assert key in counts or counts.get(key, 0) == 0

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_value_increment(counts, key, max_value):
    original_value = counts.get(key, 0)
    track_deployment(counts, key, max_value=max_value)
    if max_value is None or original_value + 1 <= max_value:
        assert counts[key] == original_value + 1
    else:
        assert counts[key] == max_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_new_value_computation(counts, key, max_value):
    original_value = counts.get(key, 0)
    new_value = original_value + 1
    track_deployment(counts, key, max_value=max_value)
    assert counts[key] == new_value

@given(counts=st.dictionaries(st.text(), st.integers()), key=st.text(), max_value=st.integers())
def test_max_value_check(counts, key, max_value):
    original_value = counts.get(key, 0)
    new_value = original_value + 1
    if max_value is not None and new_value > max_value:
        track_deployment(counts, key, max_value=max_value)
        assert counts[key] == max_value
    else:
        track_deployment(counts, key, max_value=max_value)
        assert counts[key] == new_value