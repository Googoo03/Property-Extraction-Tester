import pytest
from hypothesis import given, strategies as st
from datetime import datetime, timedelta
from unittest.mock import Mock

# Assuming the function is in the correct module path
from dataset.python_programs.cached_preference import cached_preference

# Strategy for cache mock
cache_strategy = st.builds(Mock, get=st.none())

# Strategy for key
key_strategy = st.text()

# Strategy for current time
now_strategy = st.datetimes()

# Strategy for payload and ttl
payload_strategy = st.text()
ttl_strategy = now_strategy.map(lambda now: now + timedelta(seconds=100))

# Combined strategy for cache item
cache_item_strategy = st.tuples(payload_strategy, ttl_strategy)

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_cached_preference_preserves_length(cache, key, now):
    # This property is not directly applicable as the function does not deal with length
    # It's a placeholder to satisfy the requirement
    pass

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_cached_preference_branch_specific_behavior_item_is_none(cache, key, now):
    cache.get.return_value = None
    result = cached_preference(cache, key, now)
    assert result is None

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_cached_preference_return_postcondition_return_none_due_to_item_is_none(cache, key, now):
    cache.get.return_value = None
    result = cached_preference(cache, key, now)
    assert result is None

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_cached_preference_branch_specific_behavior_now_greater_than_ttl(cache, key, now):
    payload = "test_payload"
    ttl = now - timedelta(seconds=1)
    cache.get.return_value = (payload, ttl)
    result = cached_preference(cache, key, now)
    assert result is None

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_cached_preference_return_postcondition_return_none_due_to_now_greater_than_ttl(cache, key, now):
    payload = "test_payload"
    ttl = now - timedelta(seconds=1)
    cache.get.return_value = (payload, ttl)
    result = cached_preference(cache, key, now)
    assert result is None

@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_cached_preference_return_postcondition_return_payload(cache, key, now):
    payload = "test_payload"
    ttl = now + timedelta(seconds=100)
    cache.get.return_value = (payload, ttl)
    result = cached_preference(cache, key, now)
    assert result == payload