import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.track_release import track_release

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_preserves_length(counters, key, cap):
    input_len = len(counters)
    track_release(counters, key, cap=cap)
    assert len(counters) == input_len

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.integers(min_value=0)
)
def test_branch_specific_behavior_cap_is_not_none(counters, key, cap):
    track_release(counters, key, cap=cap)

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.integers(min_value=0)
)
def test_branch_specific_behavior_updated_greater_than_cap(counters, key, cap):
    counters[key] = cap - 1
    track_release(counters, key, cap=cap)

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_return_postcondition(counters, key, cap):
    current = counters.get(key, 0)
    updated = current + 1 if cap is None else min(current + 1, cap)
    assert track_release(counters, key, cap=cap) == updated

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_precondition_counters_is_dict(counters, key, cap):
    assert isinstance(counters, dict)

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_precondition_key_is_string(counters, key, cap):
    assert isinstance(key, str)

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_precondition_cap_is_int_or_none(counters, key, cap):
    assert cap is None or isinstance(cap, int)

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_precondition_cap_is_non_negative(counters, key, cap):
    if cap is not None:
        assert cap >= 0

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_postcondition_counters_updated_correctly(counters, key, cap):
    input_counters = counters.copy()
    current = input_counters.get(key, 0)
    updated = current + 1 if cap is None else min(current + 1, cap)
    track_release(counters, key, cap=cap)
    assert counters[key] == updated

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_postcondition_counters_other_keys_unchanged(counters, key, cap):
    input_counters = counters.copy()
    track_release(counters, key, cap=cap)
    for k in input_counters:
        if k != key:
            assert counters[k] == input_counters[k]

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_postcondition_return_value_correct(counters, key, cap):
    current = counters.get(key, 0)
    updated = current + 1 if cap is None else min(current + 1, cap)
    return_value = track_release(counters, key, cap=cap)
    assert return_value == updated

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_postcondition_cap_respected(counters, key, cap):
    track_release(counters, key, cap=cap)
    current = counters.get(key, 0)
    if cap is not None:
        assert current <= cap
    else:
        assert current == counters.get(key, 0) + 1

@given(
    counters=st.dictionaries(st.text(), st.integers()),
    key=st.text(),
    cap=st.none() | st.integers(min_value=0)
)
def test_postcondition_increment_logic_correct(counters, key, cap):
    current = counters.get(key, 0)
    expected_updated = current + 1 if cap is None else min(current + 1, cap)
    track_release(counters, key, cap=cap)
    assert counters[key] == expected_updated