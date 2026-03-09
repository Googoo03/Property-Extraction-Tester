import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.prediction_cache import prediction_cache

@given(
    store=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_preserves_length(store, key, now):
    output = prediction_cache(store, key, now)
    # Since the function returns a single value, the length property does not apply in the traditional sense.
    # However, we can ensure that the output is a single value.
    assert isinstance(output, (type(None), int))

@given(
    store=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_branch_record_is_none(store, key, now):
    if key not in store:
        output = prediction_cache(store, key, now)
        assert output is None

@given(
    store=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_return_postcondition_default(store, key, now):
    if key not in store:
        output = prediction_cache(store, key, now)
        assert output is None
    else:
        value, deadline = store[key]
        if now > deadline:
            output = prediction_cache(store, key, now)
            assert output is None

@given(
    store=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_branch_now_greater_than_deadline(store, key, now):
    if key in store:
        value, deadline = store[key]
        if now > deadline:
            output = prediction_cache(store, key, now)
            assert output is None

@given(
    store=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_return_postcondition_value(store, key, now):
    if key in store:
        value, deadline = store[key]
        if now <= deadline:
            output = prediction_cache(store, key, now)
            assert output == value

@given(
    store=st.dictionaries(
        st.text(),
        st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_boundary_now_equals_deadline(store, key, now):
    if key in store:
        value, deadline = store[key]
        if now == deadline:
            output = prediction_cache(store, key, now)
            assert output == value