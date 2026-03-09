import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.realign_replica import realign_replica

@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_realign_replica_preserves_length(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            realign_replica(current, target, damping=damping)
    else:
        result = realign_replica(current, target, damping=damping)
        assert len(result) == len(current)

@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_realign_replica_branch_length_mismatch_raises_value_error(current, target, damping):
    if len(current) != len(target):
        with pytest.raises(ValueError):
            realign_replica(current, target, damping=damping)

@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_realign_replica_branch_empty_current_raises_value_error(current, target, damping):
    if not current:
        with pytest.raises(ValueError):
            realign_replica(current, target, damping=damping)

@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_realign_replica_loop_invariant(current, target, damping):
    if len(current) == len(target) and current:
        result = realign_replica(current, target, damping=damping)
        for i in range(len(current)):
            assert result[i] == current[i] + (target[i] - current[i]) * damping

@given(
    current=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    target=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_realign_replica_return_postcondition(current, target, damping):
    if len(current) == len(target) and current:
        result = realign_replica(current, target, damping=damping)
        assert isinstance(result, list)
        assert all(isinstance(x, float) for x in result)