import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.bump_click import bump_click

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserves_length(counters, key, cap):
    input_len = len(counters)
    output = bump_click(counters, key, cap=cap)
    assert len(counters) == input_len

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior(counters, key, cap):
    counters_copy = counters.copy()
    cap = cap if cap is not None else 0
    output = bump_click(counters, key, cap=cap)
    if cap is not None and counters_copy.get(key, 0) > cap:
        assert counters[key] == cap
    else:
        assert counters[key] == counters_copy.get(key, 0) + 1

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    output = bump_click(counters, key, cap=cap)
    assert output == counters[key]

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_clamping_behavior(counters, key, cap):
    cap = cap if cap is not None else 0
    output = bump_click(counters, key, cap=cap)
    if cap is not None and counters.get(key, 0) >= cap:
        assert counters[key] == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_initialization(counters, key, cap):
    initial_value = counters.get(key, 0)
    output = bump_click(counters, key, cap=cap)
    if initial_value == 0:
        assert counters[key] == 1

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_increment(counters, key, cap):
    initial_value = counters.get(key, 0)
    output = bump_click(counters, key, cap=cap)
    if cap is None or initial_value < cap:
        assert counters[key] == initial_value + 1