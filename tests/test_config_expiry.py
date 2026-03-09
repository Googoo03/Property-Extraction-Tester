from hypothesis import given
from hypothesis import strategies as st
import pytest

from dataset.python_programs.config_expiry import config_expiry

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_preserves_length(entries, key, now):
    result = config_expiry(entries, key, now)
    assert len(entries) == len(entries)

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_branch_specific_behavior_key_not_in_entries(entries, key, now):
    if key not in entries:
        assert config_expiry(entries, key, now) is None

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_return_postcondition(entries, key, now):
    if key not in entries or now > entries.get(key, (None, None))[1]:
        assert config_expiry(entries, key, now) is None

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_branch_specific_behavior_now_greater_than_expires_at(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now > expires_at:
            assert config_expiry(entries, key, now) is None

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_return_postcondition_key_in_entries_and_now_less_than_or_equal_to_expires_at(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now <= expires_at:
            assert config_expiry(entries, key, now) == value