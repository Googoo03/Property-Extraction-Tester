import pytest
from hypothesis import given, strategies as st
from datetime import datetime

# Assuming the function is in dataset/python_programs/token_expiry_check.py
from dataset.python_programs.token_expiry_check import token_expiry_check

# Property: preserves_length
@given(tokens=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_preserves_length(tokens, key, now):
    tokens_copy = tokens.copy()
    token_expiry_check(tokens, key, now)
    assert len(tokens) == len(tokens_copy)

# Property: branch_specific_behavior when record is None
@given(tokens=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_branch_specific_behavior_record_none(tokens, key, now):
    if key not in tokens:
        assert token_expiry_check(tokens, key, now) is None

# Property: return_postcondition when record is None
@given(tokens=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_postcondition_record_none(tokens, key, now):
    if key not in tokens:
        assert token_expiry_check(tokens, key, now) is None

# Property: branch_specific_behavior when now > expires_at
@given(tokens=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_branch_specific_behavior_now_greater_than_expires_at(tokens, key, now):
    if key in tokens:
        _, expires_at = tokens[key]
        if now > expires_at:
            assert token_expiry_check(tokens, key, now) is None

# Property: return_postcondition when now > expires_at
@given(tokens=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_postcondition_now_greater_than_expires_at(tokens, key, now):
    if key in tokens:
        _, expires_at = tokens[key]
        if now > expires_at:
            assert token_expiry_check(tokens, key, now) is None

# Property: return_postcondition when now <= expires_at
@given(tokens=st.dictionaries(st.text(), st.tuples(st.text(), st.datetimes())), key=st.text(), now=st.datetimes())
def test_return_postcondition_now_less_than_or_equal_to_expires_at(tokens, key, now):
    if key in tokens:
        value, expires_at = tokens[key]
        if now <= expires_at:
            assert token_expiry_check(tokens, key, now) == value