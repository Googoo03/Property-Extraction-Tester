import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.lr_warmup_schedule import lr_warmup_schedule

@given(step=st.integers(min_value=0), base_lr=st.floats(min_value=0, max_value=1e6), warmup_steps=st.integers(min_value=1))
def test_preserve_length(step, base_lr, warmup_steps):
    output = lr_warmup_schedule(step, base_lr=base_lr, warmup_steps=warmup_steps)
    assert len([output]) == 1

@given(warmup_steps=st.integers(max_value=0))
def test_branch_specific_behavior_warmup_steps(warmup_steps):
    with pytest.raises(ValueError):
        lr_warmup_schedule(0, warmup_steps=warmup_steps)

@given(step=st.integers(max_value=-1))
def test_branch_specific_behavior_step(step):
    with pytest.raises(ValueError):
        lr_warmup_schedule(step, warmup_steps=100)

@given(step=st.integers(min_value=100), base_lr=st.floats(min_value=0, max_value=1e6), warmup_steps=st.integers(min_value=100))
def test_branch_specific_behavior_step_ge_warmup_steps(step, base_lr, warmup_steps):
    assert lr_warmup_schedule(step, base_lr=base_lr, warmup_steps=warmup_steps) == base_lr

@given(base_lr=st.floats(min_value=0, max_value=1e6), warmup_steps=st.integers(min_value=1))
def test_return_postcondition_base_lr(base_lr, warmup_steps):
    step = warmup_steps
    output = lr_warmup_schedule(step, base_lr=base_lr, warmup_steps=warmup_steps)
    assert output == base_lr

@given(step=st.integers(min_value=0, max_value=99), base_lr=st.floats(min_value=0, max_value=1e6), warmup_steps=st.integers(min_value=100))
def test_return_postcondition_scaled_lr(step, base_lr, warmup_steps):
    expected = base_lr * (step / warmup_steps)
    output = lr_warmup_schedule(step, base_lr=base_lr, warmup_steps=warmup_steps)
    assert output == expected