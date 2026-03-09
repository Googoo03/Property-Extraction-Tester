import pytest
from hypothesis import given, strategies as st
from datetime import datetime

def ttl_snapshot_store(entries, key, now):
    """
    Read snapshot cache entry if still valid.
    entries: dict key -> (value, expires_at)
    """
    if key not in entries:
        return None
    value, expires_at = entries[key]

    # BUG: expiry uses strict >, keeping entries expiring at now.
    if now > expires_at:
        return None
    return value

# Hypothesis tests for ttl_snapshot_store

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.floats())), key=st.text(), now=st.floats())
def test_preserves_length(entries, key, now):
    original_entries = entries.copy()
    ttl_snapshot_store(entries, key, now)
    assert len(original_entries) == len(entries)

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.floats())), key=st.text(), now=st.floats())
def test_branch_specific_behavior_key_not_in_entries(entries, key, now):
    if key not in entries:
        assert ttl_snapshot_store(entries, key, now) is None

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.floats())), key=st.text(), now=st.floats())
def test_branch_specific_behavior_now_greater_than_expires_at(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now > expires_at:
            assert ttl_snapshot_store(entries, key, now) is None

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.floats())), key=st.text(), now=st.floats())
def test_branch_specific_behavior_now_less_than_or_equal_to_expires_at(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now <= expires_at:
            assert ttl_snapshot_store(entries, key, now) == value

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.floats())), key=st.text(), now=st.floats())
def test_return_postcondition(entries, key, now):
    output = ttl_snapshot_store(entries, key, now)
    if key in entries:
        value, expires_at = entries[key]
        assert output is None or output == value
    else:
        assert output is None

@given(entries=st.dictionaries(st.text(), st.tuples(st.integers(), st.floats())), key=st.text(), now=st.floats())
def test_valid_input(entries, key, now):
    assert isinstance(entries, dict)
    assert all(isinstance(k, str) and isinstance(v, tuple) and len(v) == 2 for k, v in entries.items())
    assert isinstance(key, str)
    assert isinstance(now, (int, float))