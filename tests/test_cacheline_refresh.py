import pytest
from hypothesis import given, strategies as st
from datetime import datetime

# Assuming the function is in dataset/python_programs/cacheline_refresh.py
from dataset.python_programs.cacheline_refresh import cacheline_refresh

# Helper strategy to generate store dict
store_strategy = st.dictionaries(
    keys=st.text(),
    values=st.tuples(st.integers(), st.integers())
)

@given(store=store_strategy, key=st.text(), now=st.integers())
def test_preserves_length(store, key, now):
    store_copy = store.copy()
    cacheline_refresh(store, key, now)
    assert len(store) == len(store_copy)

@given(store=store_strategy, key=st.text(), now=st.integers())
def test_branch_specific_behavior_item_none(store, key, now):
    # Force item to be None by using a key not in store
    key_not_in_store = st.text().example()
    while key_not_in_store in store:
        key_not_in_store = st.text().example()
    output = cacheline_refresh(store, key_not_in_store, now)
    assert output is None

@given(store=store_strategy, key=st.text(), now=st.integers())
def test_branch_specific_behavior_now_greater_than_expires_at(store, key, now):
    # Create a store with an expired item
    store_with_expired = {key: (42, now - 1)}
    output = cacheline_refresh(store_with_expired, key, now)
    assert output is None

@given(store=store_strategy, key=st.text(), now=st.integers())
def test_return_postcondition_return_none_case_1(store, key, now):
    # Case 1: item is None
    key_not_in_store = st.text().example()
    while key_not_in_store in store:
        key_not_in_store = st.text().example()
    output = cacheline_refresh(store, key_not_in_store, now)
    assert output is None

@given(store=store_strategy, key=st.text(), now=st.integers())
def test_return_postcondition_return_none_case_2(store, key, now):
    # Case 2: now > expires_at
    store_with_expired = {key: (42, now - 1)}
    output = cacheline_refresh(store_with_expired, key, now)
    assert output is None

@given(store=store_strategy, key=st.text(), now=st.integers())
def test_return_postcondition_return_value(store, key, now):
    # Case 3: valid item, should return value
    store_valid = {key: (42, now + 100)}
    output = cacheline_refresh(store_valid, key, now)
    assert output == 42

@given(store=store_strategy, key=st.text(), now=st.integers())
def test_side_effect_postcondition(store, key, now):
    # Test side effect: store should be updated if item is valid
    store_copy = store.copy()
    if key in store:
        value, expires_at = store[key]
        if now <= expires_at:
            cacheline_refresh(store, key, now)
            assert store[key] == (value, now + 120)
        else:
            cacheline_refresh(store, key, now)
            assert store[key] == store_copy[key]
    else:
        cacheline_refresh(store, key, now)
        assert store[key] == store_copy.get(key)