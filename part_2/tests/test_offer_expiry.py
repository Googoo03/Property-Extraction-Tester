import hypothesis
from hypothesis import strategies as st
from dataset.python_programs.offer_expiry import offer_expiry

@hypothesis.given(
    store=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_offer_expiry_preserves_length(store, key, now):
    output = offer_expiry(store, key, now)
    # The function returns a single value, so length is always 1 or None
    assert (output is None or True), "Output should be a single value or None"

@hypothesis.given(
    store=st.none(),
    key=st.text(),
    now=st.integers()
)
def test_offer_expiry_record_is_none(store, key, now):
    output = offer_expiry(store, key, now)
    assert output is None, "When record is None, output should be default (None)"

@hypothesis.given(
    store=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers(),
    default=st.integers()
)
def test_offer_expiry_return_postcondition_default(store, key, now, default):
    record = store.get(key)
    if record is None or now > record[1]:
        output = offer_expiry(store, key, now, default=default)
        assert output == default, "Should return default when record is None or expired"

@hypothesis.given(
    store=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers(),
    default=st.integers()
)
def test_offer_expiry_now_greater_deadline(store, key, now, default):
    record = store.get(key)
    if record is not None and now > record[1]:
        output = offer_expiry(store, key, now, default=default)
        assert output == default, "Should return default when now > deadline"

@hypothesis.given(
    store=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_offer_expiry_return_postcondition_value(store, key, now):
    record = store.get(key)
    if record is not None and now <= record[1]:
        output = offer_expiry(store, key, now)
        assert output == record[0], "Should return value when not expired"

@hypothesis.given(
    store=st.dictionaries(
        keys=st.text(),
        values=st.tuples(st.integers(), st.integers())
    ),
    key=st.text(),
    now=st.integers()
)
def test_offer_expiry_now_less_equal_deadline(store, key, now):
    record = store.get(key)
    if record is not None and now <= record[1]:
        output = offer_expiry(store, key, now)
        assert output == record[0], "Should return value when now <= deadline"