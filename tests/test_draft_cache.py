from hypothesis import given, strategies as st
import pytest
from datetime import datetime

# Assuming the function is in a file named 'draft_cache.py' in the dataset/python_programs directory
from dataset.python_programs.draft_cache import draft_cache

# Property: preserves_length
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_preserves_length(entries, key, now):
    result = draft_cache(entries, key, now)
    assert len(entries) == len(entries)

# Property: branch_specific_behavior (key not in entries)
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_branch_key_not_in_entries(entries, key, now):
    if key not in entries:
        result = draft_cache(entries, key, now)
        assert result is None

# Property: branch_specific_behavior (now > expires_at)
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_branch_now_greater_than_expires_at(entries, key, now):
    if key in entries:
        _, expires_at = entries[key]
        if now > expires_at:
            result = draft_cache(entries, key, now)
            assert result is None

# Property: return_postcondition
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_postcondition(entries, key, now):
    result = draft_cache(entries, key, now)
    if result is not None:
        assert result == entries[key][0]