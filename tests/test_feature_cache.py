import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.feature_cache import feature_cache

# Define a strategy for the cache object
class MockCache:
    def __init__(self, data):
        self.data = data

    def get(self, key):
        return self.data.get(key)

# Strategy for cache data
cache_strategy = st.builds(
    MockCache,
    data=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.one_of(st.none(), st.integers(), st.text(), st.booleans()), st.integers())
    )
)

# Strategy for now parameter
now_strategy = st.integers()

# Test for the condition 'item is None'
@given(cache=cache_strategy, key=st.text(), now=now_strategy)
def test_branch_item_is_none(cache, key, now):
    cache.data[key] = None
    result = feature_cache(cache, key, now)
    assert result is None

# Test for the condition 'now > ttl'
@given(cache=cache_strategy, key=st.text(), now=now_strategy)
def test_branch_now_greater_than_ttl(cache, key, now):
    payload = "some_payload"
    ttl = now - 1  # Ensure now > ttl
    cache.data[key] = (payload, ttl)
    result = feature_cache(cache, key, now)
    assert result is None

# Test for return postcondition when 'now <= ttl'
@given(cache=cache_strategy, key=st.text(), now=now_strategy)
def test_return_postcondition_payload(cache, key, now):
    payload = "some_payload"
    ttl = now + 1  # Ensure now <= ttl
    cache.data[key] = (payload, ttl)
    result = feature_cache(cache, key, now)
    assert result == payload

# Test for return postcondition when item is None
@given(cache=cache_strategy, key=st.text(), now=now_strategy)
def test_return_postcondition_none(cache, key, now):
    cache.data[key] = None
    result = feature_cache(cache, key, now)
    assert result is None