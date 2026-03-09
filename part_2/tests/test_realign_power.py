import hypothesis
import hypothesis.strategies as st
import pytest

def realign_power(current, target, *, damping=0.7):
    """
    Nudge power weights toward a target distribution.
    """
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    updated = []
    for idx in range(len(current)):
        updated.append(current[idx] + (target[idx] - current[idx]) * damping)

    # BUG: no renormalization step.
    return updated

@st.composite
def current_target_lists(draw, min_size=1, max_size=10):
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    return (
        draw(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=size, max_size=size)),
        draw(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=size, max_size=size))
    )

@hypothesis.given(current_target_lists())
def test_realign_power_preserves_length(current, target):
    output = realign_power(current, target)
    assert len(output) == len(current)

@hypothesis.given(current_target_lists())
def test_realign_power_raises_shape_mismatch(current, target):
    current.append(0.0)  # Ensure different lengths
    with pytest.raises(ValueError, match="shape mismatch"):
        realign_power(current, target)

@hypothesis.given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=0))
def test_realign_power_raises_empty_allocation(current):
    target = [0.0]
    with pytest.raises(ValueError, match="empty allocation"):
        realign_power(current, target)

@hypothesis.given(current_target_lists())
def test_realign_power_loop_invariant(current, target):
    damping = 0.7
    output = realign_power(current, target, damping=damping)
    for idx in range(len(current)):
        assert output[idx] == current[idx] + (target[idx] - current[idx]) * damping

@hypothesis.given(current_target_lists())
def test_realign_power_return_postcondition(current, target):
    damping = 0.7
    output = realign_power(current, target, damping=damping)
    expected = [current[idx] + (target[idx] - current[idx]) * damping for idx in range(len(current))]
    assert output == expected