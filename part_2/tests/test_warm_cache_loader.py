import pytest
from hypothesis import given, strategies as st
from datetime import datetime
from dataset.python_programs.warm_cache_loader import warm_cache_loader

# Property: preserves_length
@given(
    cache=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.integers())),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_preserves_length(cache, key, now, ttl):
    cache_copy = cache.copy()
    warm_cache_loader(cache, key, now, ttl=ttl)
    assert len(cache_copy) == len(cache)

# Property: branch_specific_behavior (item is None)
@given(
    cache=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.integers())),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_branch_item_none(cache, key, now, ttl):
    assert warm_cache_loader(cache, key, now, ttl=ttl) is None

# Property: return_postcondition (item is None)
@given(
    cache=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.integers())),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_return_item_none(cache, key, now, ttl):
    assert warm_cache_loader(cache, key, now, ttl=ttl) is None

# Property: branch_specific_behavior (now > expires_at)
@given(
    cache=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.integers())),
    key=st.text(),
    now=st.integers(min_value=1),
    ttl=st.integers()
)
def test_branch_now_greater_than_expires_at(cache, key, now, ttl):
    # Ensure now > expires_at
    cache[key] = (None, now - 1)
    assert warm_cache_loader(cache, key, now, ttl=ttl) is None

# Property: return_postcondition (now > expires_at)
@given(
    cache=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.integers())),
    key=st.text(),
    now=st.integers(min_value=1),
    ttl=st.integers()
)
def test_return_now_greater_than_expires_at(cache, key, now, ttl):
    cache[key] = (None, now - 1)
    assert warm_cache_loader(cache, key, now, ttl=ttl) is None

# Property: return_postcondition (valid cache entry)
@given(
    cache=st.dictionaries(st.text(), st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.integers())),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_return_valid_cache_entry(cache, key, now, ttl):
    value = "test_value"
    expires_at = now + ttl + 1  # Ensure valid cache entry
    cache[key] = (value, expires_at)
    assert warm_cache_loader(cache, key, now, ttl=ttl) == value