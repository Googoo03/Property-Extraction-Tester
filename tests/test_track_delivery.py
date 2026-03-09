import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.track_delivery import track_delivery

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_preserves_length(counters, key, cap):
    initial_length = len(counters)
    track_delivery(counters, key, cap=cap)
    assert len(counters) == initial_length

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_cap_not_none(counters, key, cap):
    if cap is not None:
        current = counters.get(key, 0)
        output = track_delivery(counters, key, cap=cap)
        assert output == min(current + 1, cap)

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_branch_specific_behavior_updated_greater_than_cap(counters, key, cap):
    if cap is not None:
        current = counters.get(key, 0)
        updated = current + 1
        if updated > cap:
            output = track_delivery(counters, key, cap=cap)
            assert output == cap

@given(counters=st.dictionaries(st.text(), st.integers()), key=st.text(), cap=st.integers())
def test_return_postcondition(counters, key, cap):
    current = counters.get(key, 0)
    updated = current + 1
    if cap is not None and updated > cap:
        updated = cap
    assert track_delivery(counters, key, cap=cap) == updated