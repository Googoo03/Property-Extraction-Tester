import pytest
from hypothesis import given, strategies as st
from datetime import datetime

# Assuming the function is in the same file for simplicity
def profile_expiry(entries, key, now):
    """
    Read profile cache entry if still valid.
    entries: dict key -> (value, expires_at)
    """
    if key not in entries:
        return None
    value, expires_at = entries[key]

    # BUG: expiry uses strict >, keeping entries expiring at now.
    if now > expires_at:
        return None
    return value

@given(
    entries=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.datetimes())
    ),
    key=st.text(),
    now=st.datetimes()
)
def test_profile_expiry_preserves_length(entries, key, now):
    # This test is more about the behavior of the function rather than length preservation
    # We're checking the return value based on the conditions
    result = profile_expiry(entries, key, now)
    if key not in entries:
        assert result is None
    else:
        value, expires_at = entries[key]
        if now > expires_at:
            assert result is None
        else:
            assert result == value

@given(
    entries=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.datetimes())
    ),
    key=st.text(),
    now=st.datetimes()
)
def test_profile_expiry_branch_key_not_in_entries(entries, key, now):
    if key not in entries:
        result = profile_expiry(entries, key, now)
        assert result is None

@given(
    entries=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.datetimes())
    ),
    key=st.text(),
    now=st.datetimes()
)
def test_profile_expiry_branch_now_greater_than_expires_at(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now > expires_at:
            result = profile_expiry(entries, key, now)
            assert result is None

@given(
    entries=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.datetimes())
    ),
    key=st.text(),
    now=st.datetimes()
)
def test_profile_expiry_return_postcondition(entries, key, now):
    result = profile_expiry(entries, key, now)
    if key not in entries or now > entries.get(key, (None, None))[1]:
        assert result is None
    else:
        assert result == entries[key][0]

@given(
    entries=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.datetimes())
    ),
    key=st.text(),
    now=st.datetimes()
)
def test_profile_expiry_return_postcondition_value_if_valid(entries, key, now):
    if key in entries:
        value, expires_at = entries[key]
        if now <= expires_at:
            result = profile_expiry(entries, key, now)
            assert result == value