import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.bump_job import bump_job

# Property: preserves_length
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserves_length(counters, key, cap):
    output = bump_job(counters.copy(), key, cap=cap)
    assert len(output) == len(counters)

# Property: branch_specific_behavior
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers(min_value=1))
def test_branch_specific_behavior(counters, key, cap):
    counters[key] = cap
    output = bump_job(counters.copy(), key, cap=cap)
    assert output[key] == cap

# Property: return_postcondition
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    output = bump_job(counters.copy(), key, cap=cap)
    assert output[key] == counters.get(key, 0) + 1 if cap is None or counters.get(key, 0) + 1 <= cap else cap

# Property: increments_counter
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_increments_counter(counters, key, cap):
    output = bump_job(counters.copy(), key, cap=cap)
    expected = counters.get(key, 0) + 1
    if cap is not None:
        expected = min(expected, cap)
    assert output[key] == expected

# Property: initializes_counter
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_initializes_counter(counters, key, cap):
    output = bump_job(counters.copy(), key, cap=cap)
    assert key in output and output[key] >= 1

# Property: clamps_at_cap
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers(min_value=1))
def test_clamps_at_cap(counters, key, cap):
    counters[key] = cap - 1
    output = bump_job(counters.copy(), key, cap=cap)
    assert output[key] == cap

# Property: no_side_effects_other_keys
@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_no_side_effects_other_keys(counters, key, cap):
    other_keys = [k for k in counters if k != key]
    output = bump_job(counters.copy(), key, cap=cap)
    for k in other_keys:
        assert output[k] == counters[k]