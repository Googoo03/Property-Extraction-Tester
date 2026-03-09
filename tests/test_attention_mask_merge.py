import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.attention_mask_merge import attention_mask_merge

@given(mask_a=st.lists(st.booleans()), mask_b=st.lists(st.booleans()))
def test_preserves_length(mask_a, mask_b):
    if len(mask_a) == len(mask_b):
        output = attention_mask_merge(mask_a, mask_b)
        assert len(output) == len(mask_a)

@given(mask_a=st.lists(st.booleans()), mask_b=st.lists(st.booleans()))
def test_branch_specific_behavior(mask_a, mask_b):
    if len(mask_a) != len(mask_b):
        with pytest.raises(ValueError, match="shape mismatch"):
            attention_mask_merge(mask_a, mask_b)

@given(mask_a=st.lists(st.booleans()), mask_b=st.lists(st.booleans()))
def test_loop_invariant(mask_a, mask_b):
    if len(mask_a) == len(mask_b):
        merged = attention_mask_merge(mask_a, mask_b)
        assert all(merged[i] == (mask_a[i] or mask_b[i]) for i in range(len(merged)))

@given(mask_a=st.lists(st.booleans()), mask_b=st.lists(st.booleans()))
def test_return_postcondition(mask_a, mask_b):
    if len(mask_a) == len(mask_b):
        merged = attention_mask_merge(mask_a, mask_b)
        assert all(merged[i] == (mask_a[i] or mask_b[i]) for i in range(len(merged)))