import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.load_mix import load_mix

# Property: preserves_length
@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            load_mix(current, target, damping=damping)
    else:
        result = load_mix(current, target, damping=damping)
        assert len(result) == len(current)

# Property: branch_specific_behavior (length mismatch)
@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_length_mismatch(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            load_mix(current, target, damping=damping)

# Property: branch_specific_behavior (empty current)
@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=0),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_empty_current(current, target, damping):
    with pytest.raises(ValueError):
        load_mix(current, target, damping=damping)

# Property: loop_invariant
@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_loop_invariant(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            load_mix(current, target, damping=damping)
    else:
        result = load_mix(current, target, damping=damping)
        for c, t, a in zip(current, target, result):
            assert a == c + (t - c) * damping

# Property: return_postcondition
@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_return_postcondition(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            load_mix(current, target, damping=damping)
    else:
        result = load_mix(current, target, damping=damping)
        assert isinstance(result, list)
        assert len(result) == len(current)