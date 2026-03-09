import pytest
from hypothesis import given, strategies as st
from datetime import datetime

# Assuming the function is in the specified directory
from dataset.python_programs.embedding_lookup_cache import embedding_lookup_cache

# Test for property: preserves_length (len(output) == len(input))
@given(
    cache=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_preserves_length(cache, key, now, ttl):
    result = embedding_lookup_cache(cache, key, now, ttl=ttl)
    # This property doesn't make sense for this function as it returns a single value or None
    # We'll just check that the result is either the cached value or None
    if key in cache:
        assert result == cache[key][0] or result is None
    else:
        assert result is None

# Test for branch-specific behavior: item is None
@given(
    cache=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_branch_item_is_none(cache, key, now, ttl):
    # Ensure key is not in cache to trigger the branch
    cache = {k: v for k, v in cache.items() if k != key}
    result = embedding_lookup_cache(cache, key, now, ttl=ttl)
    assert result is None

# Test for return postcondition: returns value satisfying expected semantics (return None)
@given(
    cache=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_return_postcondition_none(cache, key, now, ttl):
    # Ensure key is in cache but expired to trigger None return
    if key not in cache:
        cache[key] = (123, now - ttl - 1)
    else:
        cached_value, cached_at = cache[key]
        cache[key] = (cached_value, now - ttl - 1)
    result = embedding_lookup_cache(cache, key, now, ttl=ttl)
    assert result is None

# Test for branch-specific behavior: now > cached_at + ttl
@given(
    cache=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_branch_now_greater_than_cached_at_plus_ttl(cache, key, now, ttl):
    # Ensure key is in cache and expired
    if key not in cache:
        cache[key] = (123, now - ttl - 1)
    else:
        cached_value, cached_at = cache[key]
        cache[key] = (cached_value, now - ttl - 1)
    result = embedding_lookup_cache(cache, key, now, ttl=ttl)
    assert result is None

# Test for return postcondition: returns value satisfying expected semantics (return value)
@given(
    cache=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers(),
    ttl=st.integers()
)
def test_return_postcondition_value(cache, key, now, ttl):
    # Ensure key is in cache and not expired
    if key not in cache:
        cache[key] = (123, now)
    else:
        cached_value, cached_at = cache[key]
        cache[key] = (cached_value, now)
    result = embedding_lookup_cache(cache, key, now, ttl=ttl)
    assert result == cache[key][0]