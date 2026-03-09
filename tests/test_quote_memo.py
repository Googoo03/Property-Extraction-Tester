import hypothesis
from hypothesis import given, strategies as st
import pytest
from datetime import datetime, timedelta
from dataset.python_programs.quote_memo import quote_memo

# Strategy for cache items
cache_strategy = st.dictionaries(
    st.text(),
    st.tuples(st.binary(), st.datetimes())
)

# Strategy for keys
key_strategy = st.text()

# Strategy for current time
now_strategy = st.datetimes()

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_quote_memo_preserves_length(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        output = quote_memo(cache, key, now)
        assert len(output) == len(payload) if output is not None else True

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_quote_memo_branch_item_is_none(cache, key, now):
    item = cache.get(key)
    output = quote_memo(cache, key, now)
    if item is None:
        assert output is None

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_quote_memo_return_postcondition_return_none_due_to_expiry(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now > ttl:
            output = quote_memo(cache, key, now)
            assert output is None

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_quote_memo_return_postcondition_return_payload(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now <= ttl:
            output = quote_memo(cache, key, now)
            assert output == payload