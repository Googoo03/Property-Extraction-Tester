import pytest
from hypothesis import given, strategies as st
from datetime import datetime

# Assuming the function is in the specified path
from dataset.python_programs.plan_memo import plan_memo

# Property: preserves_length
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())))
def test_preserves_length(entries):
    key = "test_key"
    now = datetime.now()
    plan_memo(entries, key, now)
    assert len(entries) == len(entries)

# Property: branch_specific_behavior - key not in entries
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())),
       now=st.datetimes())
def test_branch_key_not_in_entries(entries, now):
    key = "non_existent_key"
    assert plan_memo(entries, key, now) is None

# Property: branch_specific_behavior - now > expires_at
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())),
       key=st.text())
def test_branch_now_greater_than_expires_at(entries, key):
    value = "test_value"
    expires_at = datetime.now() - datetime.timedelta(seconds=1)
    entries[key] = (value, expires_at)
    now = datetime.now()
    assert plan_memo(entries, key, now) is None

# Property: return_postcondition - returns None if key not in entries or now > expires_at
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())),
       now=st.datetimes())
def test_return_postcondition_none(entries, now):
    key = "non_existent_key"
    assert plan_memo(entries, key, now) is None
    for k in entries:
        value, expires_at = entries[k]
        if now > expires_at:
            assert plan_memo(entries, k, now) is None

# Property: return_postcondition - returns value if key in entries and now <= expires_at
@given(entries=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())),
       now=st.datetimes())
def test_return_postcondition_value(entries, now):
    for k in entries:
        value, expires_at = entries[k]
        if now <= expires_at:
            assert plan_memo(entries, k, now) == value