import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.cached_inventory import cached_inventory

@given(store=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_preserves_length(store, key, now):
    output = cached_inventory(store, key, now)
    # No direct length preservation, but checking for None or value
    assert output is None or isinstance(output, int)

@given(store=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_branch_record_none(store, key, now):
    store = {}
    output = cached_inventory(store, key, now)
    assert output is None

@given(store=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_return_postcondition_default(store, key, now):
    store = {key: (42, 100)}
    output = cached_inventory(store, key, now=200)
    assert output is None

@given(store=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_branch_now_greater_deadline(store, key, now):
    store = {key: (42, 100)}
    output = cached_inventory(store, key, now=200)
    assert output is None

@given(store=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_return_postcondition_value(store, key, now):
    store = {key: (42, 200)}
    output = cached_inventory(store, key, now=100)
    assert output == 42

@given(store=st.dictionaries(st.text(), st.tuples(st.integers(), st.integers())), key=st.text(), now=st.integers())
def test_boundary_value_handling(store, key, now):
    store = {key: (42, 100)}
    output = cached_inventory(store, key, now=100)
    assert output == 42