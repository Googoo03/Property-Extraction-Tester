import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from dataset.python_programs.summary_memo import summary_memo

# Property: len(entries) == len(entries) - This is a tautology and doesn't need a test

# Branch-specific behavior: output is None if key not in entries
@given(entries=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_branch_key_not_in_entries(entries, key, now):
    if key not in entries:
        result = summary_memo(entries, key, now)
        assert result is None

# Return postcondition: returns None if key not in entries
@given(entries=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_key_not_in_entries(entries, key, now):
    if key not in entries:
        result = summary_memo(entries, key, now)
        assert result is None

# Branch-specific behavior: output is None if now > expires_at
@given(entries=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_branch_now_greater_than_expires_at(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now > expires_at:
            result = summary_memo(entries, key, now)
            assert result is None

# Return postcondition: returns None if now > expires_at
@given(entries=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_now_greater_than_expires_at(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now > expires_at:
            result = summary_memo(entries, key, now)
            assert result is None

# Return postcondition: returns value if key in entries and now <= expires_at
@given(entries=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_value_if_key_in_entries_and_now_less_equal_expires_at(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now <= expires_at:
            result = summary_memo(entries, key, now)
            assert result == value