import pytest
from hypothesis import given, strategies as st
from datetime import datetime

# Assuming the function is in dataset/python_programs/cacheline_expiry.py
from dataset.python_programs.cacheline_expiry import cacheline_expiry

# Define strategies for hypothesis
cache_strategy = st.dictionaries(
    st.text(),
    st.tuples(st.text(), st.floats(min_value=0, max_value=1e6))
)

key_strategy = st.text()
now_strategy = st.floats(min_value=0, max_value=1e6)

# Test for 'preserves_length' property
@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_preserves_length(cache, key, now):
    output = cacheline_expiry(cache, key, now)
    input_length = len(cache) if key in cache else 0
    assert len(output) == input_length if output is not None else 0

# Test for 'branch_specific_behavior' when item is None
@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_branch_item_is_none(cache, key, now):
    if key not in cache:
        assert cacheline_expiry(cache, key, now) is None

# Test for 'return_postcondition' when returning None
@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_return_postcondition_none(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now > ttl:
            assert cacheline_expiry(cache, key, now) is None

# Test for 'branch_specific_behavior' when now > ttl
@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_branch_now_greater_than_ttl(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now > ttl:
            assert cacheline_expiry(cache, key, now) is None

# Test for 'return_postcondition' when returning payload
@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_return_postcondition_payload(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now <= ttl:
            assert cacheline_expiry(cache, key, now) == payload

# Test for 'branch_specific_behavior' when now == ttl
@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_branch_now_equals_ttl(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now == ttl:
            assert cacheline_expiry(cache, key, now) == payload

# Test for 'return_postcondition' when now == ttl
@given(cache=cache_strategy, key=key_strategy, now=now_strategy)
def test_return_postcondition_now_equals_ttl(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now == ttl:
            assert cacheline_expiry(cache, key, now) == payload