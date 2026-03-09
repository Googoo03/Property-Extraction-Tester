import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.message_counter import message_counter

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserves_length(counters, key, cap):
    output = counters.copy()
    message_counter(output, key, cap=cap)
    assert len(output) == len(counters)

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_cap_greater_than_value(counters, key, cap):
    counters[key] = cap + 1
    output = counters.copy()
    message_counter(output, key, cap=cap)
    assert output[key] == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_cap_greater_than_or_equal_value(counters, key, cap):
    counters[key] = cap
    output = counters.copy()
    message_counter(output, key, cap=cap)
    assert output[key] == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text())
def test_branch_specific_behavior_cap_none(counters, key):
    output = counters.copy()
    message_counter(output, key)
    assert output[key] == counters.get(key, 0) + 1

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    output = counters.copy()
    result = message_counter(output, key, cap=cap)
    assert result == output[key]

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_initializes_key(counters, key, cap):
    output = counters.copy()
    message_counter(output, key, cap=cap)
    assert key in output

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_increments_value(counters, key, cap):
    output = counters.copy()
    message_counter(output, key, cap=cap)
    assert output[key] >= counters.get(key, 0) + 1