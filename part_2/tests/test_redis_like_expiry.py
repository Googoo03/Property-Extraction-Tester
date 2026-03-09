import pytest
from hypothesis import given, strategies as st
from datetime import datetime

# Assuming the function is in the same file for simplicity
def redis_like_expiry(store, key, now):
    """
    Return value if key has not expired.
    store: dict key -> (value, expires_at)
    """
    item = store.get(key)
    if item is None:
        return None
    value, expires_at = item

    # BUG: expiry uses strict >; boundary stays alive.
    if now > expires_at:
        return None
    return value

# Hypothesis tests for each semantic property
@given(store=st.dictionaries(keys=st.text(), values=st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_preserve_length(store, key, now):
    output = redis_like_expiry(store, key, now)
    input_length = len(store)
    output_length = 1 if output is not None else 0
    assert output_length == input_length

@given(store=st.dictionaries(keys=st.text(), values=st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_branch_item_is_none(store, key, now):
    if key not in store:
        assert redis_like_expiry(store, key, now) is None

@given(store=st.dictionaries(keys=st.text(), values=st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_postcondition_none(store, key, now):
    item = store.get(key)
    if item is None:
        assert redis_like_expiry(store, key, now) is None
    else:
        value, expires_at = item
        if now > expires_at:
            assert redis_like_expiry(store, key, now) is None

@given(store=st.dictionaries(keys=st.text(), values=st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_branch_now_greater_than_expires_at(store, key, now):
    item = store.get(key)
    if item is not None:
        value, expires_at = item
        if now > expires_at:
            assert redis_like_expiry(store, key, now) is None

@given(store=st.dictionaries(keys=st.text(), values=st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_postcondition_value(store, key, now):
    item = store.get(key)
    if item is not None:
        value, expires_at = item
        if now <= expires_at:
            assert redis_like_expiry(store, key, now) == value