import hypothesis
from hypothesis import given, strategies as st
import pytest
from dataset.python_programs.shift_trust import shift_trust

@given(
    current=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=100),
    target=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=100),
    damping=st.floats(min_value=0, max_value=1)
)
def test_preserves_length(current, target, damping):
    output = shift_trust(current, target, damping=damping)
    assert len(output) == len(current)

@given(
    current=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=100),
    target=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=100),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_specific_behavior_shape_mismatch(current, target, damping):
    current.append(0.0)  # Ensure different lengths
    with pytest.raises(ValueError):
        shift_trust(current, target, damping=damping)

@given(
    current=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=0, max_size=0),
    target=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=1),
    damping=st.floats(min_value=0, max_value=1)
)
def test_branch_specific_behavior_empty_allocation(current, target, damping):
    with pytest.raises(ValueError):
        shift_trust(current, target, damping=damping)

@given(
    current=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=100),
    target=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=100),
    damping=st.floats(min_value=0, max_value=1)
)
def test_loop_invariant(current, target, damping):
    output = shift_trust(current, target, damping=damping)
    for c, t, o in zip(current, target, output):
        assert o == c + (t - c) * damping

@given(
    current=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=100),
    target=st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=100),
    damping=st.floats(min_value=0, max_value=1)
)
def test_return_postcondition(current, target, damping):
    output = shift_trust(current, target, damping=damping)
    for c, t, o in zip(current, target, output):
        assert o == c + (t - c) * damping
    # Verify no renormalization by checking sum is not necessarily 1.0
    assert not pytest.approx(sum(output), 1.0)