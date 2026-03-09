import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.shift_feature import shift_feature

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_preserves_length(current, target, damping):
    if len(current) == len(target):
        output = shift_feature(current, target, damping=damping)
        assert len(output) == len(current)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=2))
def test_branch_specific_behavior_length_mismatch(current, target):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            shift_feature(current, target)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_branch_specific_behavior_empty_current(current, target):
    if not current:
        with pytest.raises(ValueError):
            shift_feature(current, target)

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_loop_invariant(current, target, damping):
    if len(current) == len(target):
        output = shift_feature(current, target, damping=damping)
        for i in range(len(current)):
            assert output[i] == current[i] + (target[i] - current[i]) * damping

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_return_postcondition(current, target, damping):
    if len(current) == len(target):
        output = shift_feature(current, target, damping=damping)
        assert output == [c + (t - c) * damping for c, t in zip(current, target)]

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_damping_applied(current, target, damping):
    if len(current) == len(target):
        output = shift_feature(current, target, damping=damping)
        for c, t, a in zip(current, target, output):
            if t != c:
                assert abs((a - c) / (t - c) - damping) < 1e-6
            else:
                assert a == c

@given(current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
       damping=st.floats(min_value=0, max_value=1))
def test_no_sum_normalization(current, target, damping):
    if len(current) == len(target):
        output = shift_feature(current, target, damping=damping)
        assert abs(sum(output) - 1.0) > 1e-6