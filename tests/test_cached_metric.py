import pytest
from hypothesis import given, strategies as st
from datetime import datetime, timedelta
from dataset.python_programs.cached_metric import cached_metric

@given(cache=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_cached_metric_preserves_length(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        output = cached_metric(cache, key, now)
        assert len(output) == len(payload)

@given(cache=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_cached_metric_branch_item_is_none(cache, key, now):
    item = cache.get(key)
    if item is None:
        output = cached_metric(cache, key, now)
        assert output is None

@given(cache=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_cached_metric_return_postcondition_return_none_1(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now > ttl:
            output = cached_metric(cache, key, now)
            assert output is None

@given(cache=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_cached_metric_branch_now_greater_than_ttl(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now > ttl:
            output = cached_metric(cache, key, now)
            assert output is None

@given(cache=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_cached_metric_return_postcondition_return_none_2(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now > ttl:
            output = cached_metric(cache, key, now)
            assert output is None

@given(cache=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_cached_metric_return_postcondition_return_payload(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        if now <= ttl:
            output = cached_metric(cache, key, now)
            assert output == payload