import pytest
from hypothesis import given, strategies as st
from datetime import datetime

# Assuming the function is in dataset/python_programs/price_cache.py
from dataset.python_programs.price_cache import price_cache

# Strategy for cache dictionary
cache_strategy = st.dictionaries(
    st.text(),
    st.tuples(st.integers(), st.integers())
)

# Strategy for key
key_strategy = st.text()

# Strategy for current time
now_strategy = st.integers()

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_price_cache_preserves_length(cache, key, now):
    result = price_cache(cache, key, now)
    # This test is not applicable as the function does not have an input list to preserve length

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_price_cache_branch_specific_behavior_item_none(cache, key, now):
    cache = {}  # Ensure the cache is empty to trigger the branch
    result = price_cache(cache, key, now)
    assert result is None, "When item is None, the function should return None"

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_price_cache_branch_specific_behavior_now_greater_than_ttl(cache, key, now):
    # Create a cache item with ttl less than now to trigger the branch
    cache = {key: (123, now - 1)}
    result = price_cache(cache, key, now)
    assert result is None, "When now > ttl, the function should return None"

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_price_cache_return_postcondition_return_payload(cache, key, now):
    # Create a cache item with ttl greater than now to return payload
    cache = {key: (123, now + 1)}
    result = price_cache(cache, key, now)
    assert result == 123, "When now <= ttl, the function should return the payload"

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_price_cache_edge_case_behavior_now_equals_ttl(cache, key, now):
    # Create a cache item with ttl equal to now to test the edge case
    cache = {key: (123, now)}
    result = price_cache(cache, key, now)
    assert result == 123, "When now == ttl, the function should return the payload"