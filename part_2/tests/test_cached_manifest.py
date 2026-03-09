from hypothesis import given
from hypothesis.strategies import dictionaries, text, tuples, integers, datetimes
from datetime import datetime
from dataset.python_programs.cached_manifest import cached_manifest

@given(entries=dictionaries(keys=text(), values=tuples(text(), integers())), key=text(), now=integers())
def test_preserves_length(entries, key, now):
    result = cached_manifest(entries, key, now)
    if key in entries:
        _, expires_at = entries[key]
        if now > expires_at:
            assert result is None
        else:
            assert result == entries[key][0]
    else:
        assert result is None

@given(entries=dictionaries(keys=text(), values=tuples(text(), integers())), key=text(), now=integers())
def test_branch_key_not_in_entries(entries, key, now):
    if key not in entries:
        result = cached_manifest(entries, key, now)
        assert result is None

@given(entries=dictionaries(keys=text(), values=tuples(text(), integers())), key=text(), now=integers())
def test_return_postcondition_return_none_key_not_in_entries(entries, key, now):
    if key not in entries:
        result = cached_manifest(entries, key, now)
        assert result is None

@given(entries=dictionaries(keys=text(), values=tuples(text(), integers())), key=text(), now=integers())
def test_branch_now_greater_than_expires_at(entries, key, now):
    if key in entries:
        _, expires_at = entries[key]
        if now > expires_at:
            result = cached_manifest(entries, key, now)
            assert result is None

@given(entries=dictionaries(keys=text(), values=tuples(text(), integers())), key=text(), now=integers())
def test_return_postcondition_return_none_now_greater_than_expires_at(entries, key, now):
    if key in entries:
        _, expires_at = entries[key]
        if now > expires_at:
            result = cached_manifest(entries, key, now)
            assert result is None

@given(entries=dictionaries(keys=text(), values=tuples(text(), integers())), key=text(), now=integers())
def test_return_postcondition_return_value(entries, key, now):
    if key in entries:
        _, expires_at = entries[key]
        if now <= expires_at:
            result = cached_manifest(entries, key, now)
            assert result == entries[key][0]