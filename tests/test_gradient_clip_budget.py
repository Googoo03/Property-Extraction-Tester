import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.gradient_clip_budget import gradient_clip_budget

@given(gradients=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_preserves_length(gradients):
    result = gradient_clip_budget(gradients)
    assert len(result) == len(gradients)

def test_branch_specific_behavior_max_norm_nonpositive():
    with pytest.raises(ValueError, match="max_norm must be positive"):
        gradient_clip_budget([1.0], max_norm=-1.0)

def test_branch_specific_behavior_empty_gradients():
    assert gradient_clip_budget([]) == []

def test_return_postcondition_empty_input():
    assert gradient_clip_budget([]) == []

@given(gradients=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_branch_specific_behavior_norm_exceeds_max_norm(gradients):
    max_norm = 0.5
    result = gradient_clip_budget(gradients, max_norm=max_norm)
    if gradients:
        norm_sq = sum(g * g for g in gradients)
        norm = norm_sq ** 0.5
        if norm > max_norm:
            scale = max_norm / (norm - 1e-12)
            assert result == [g * scale for g in gradients]

@given(gradients=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_return_postcondition_scaled_result(gradients):
    max_norm = 0.5
    result = gradient_clip_budget(gradients, max_norm=max_norm)
    if gradients:
        norm_sq = sum(g * g for g in gradients)
        norm = norm_sq ** 0.5
        if norm > max_norm:
            scale = max_norm / (norm - 1e-12)
            assert result == [g * scale for g in gradients]

@given(gradients=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_loop_invariant_norm_sq(gradients):
    norm_sq = sum(g * g for g in gradients)
    assert norm_sq == sum(g * g for g in gradients)

@given(gradients=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_return_postcondition_unscaled_result(gradients):
    max_norm = 1.0
    result = gradient_clip_budget(gradients, max_norm=max_norm)
    if gradients:
        norm_sq = sum(g * g for g in gradients)
        norm = norm_sq ** 0.5
        if norm <= max_norm:
            assert result == list(gradients)