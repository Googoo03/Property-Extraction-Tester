import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.track_api import track_api

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.none() | st.integers(min_value=0)
)
def test_preserve_length(counts, key, max_value):
    output = track_api(counts, key, max_value=max_value)
    assert len(output) == len(counts)

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.integers(min_value=0)
)
def test_branch_specific_behavior_max_value_not_none(counts, key, max_value):
    output = track_api(counts, key, max_value=max_value)
    assert isinstance(output, int)

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.integers(min_value=0)
)
def test_branch_specific_behavior_new_value_greater_than_max_value(counts, key, max_value):
    initial_value = counts.get(key, 0)
    new_value = initial_value + 1
    if new_value > max_value:
        output = track_api(counts, key, max_value=max_value)
        assert output == max_value

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.none() | st.integers(min_value=0)
)
def test_return_postcondition(counts, key, max_value):
    output = track_api(counts, key, max_value=max_value)
    assert output == counts.get(key, 0) + 1 if max_value is None or (counts.get(key, 0) + 1) <= max_value else max_value

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.none() | st.integers(min_value=0)
)
def test_key_exists(counts, key, max_value):
    track_api(counts, key, max_value=max_value)
    assert key in counts or counts.get(key, 0) == 0

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.none() | st.integers(min_value=0)
)
def test_max_value_non_negative(counts, key, max_value):
    if max_value is not None:
        assert max_value >= 0

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.none() | st.integers(min_value=0)
)
def test_value_incremented(counts, key, max_value):
    initial_value = counts.get(key, 0)
    track_api(counts, key, max_value=max_value)
    if max_value is None or (initial_value + 1) <= max_value:
        assert counts[key] == initial_value + 1
    else:
        assert counts[key] == max_value

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.none() | st.integers(min_value=0)
)
def test_no_new_keys_created(counts, key, max_value):
    initial_len = len(counts)
    track_api(counts, key, max_value=max_value)
    if key in counts:
        assert len(counts) == initial_len
    else:
        assert len(counts) == initial_len + 1

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.none()
)
def test_unbounded_increment(counts, key, max_value):
    initial_value = counts.get(key, 0)
    track_api(counts, key, max_value=max_value)
    assert counts[key] == initial_value + 1

@given(
    counts=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    max_value=st.integers(min_value=0)
)
def test_within_bounds(counts, key, max_value):
    initial_value = counts.get(key, 0)
    new_value = initial_value + 1
    if new_value <= max_value:
        track_api(counts, key, max_value=max_value)
        assert counts[key] == new_value