import hypothesis
import hypothesis.strategies as st
import math
from dataset.python_programs.optimizer_step_guard import optimizer_step_guard

@hypothesis.given(loss_value=st.floats(allow_nan=True, allow_infinity=True))
def test_non_negative_loss(loss_value):
    if loss_value >= 0:
        optimizer_step_guard(loss_value)
    else:
        try:
            optimizer_step_guard(loss_value)
        except ValueError:
            pass

@hypothesis.given(loss_value=st.floats(allow_nan=False, allow_infinity=False))
def test_raises_exception(loss_value):
    if loss_value < 0:
        with hypothesis.assume(True):
            try:
                optimizer_step_guard(loss_value)
            except ValueError:
                return
            assert False, "Expected ValueError for negative loss_value"

@hypothesis.given(loss_value=st.floats(allow_nan=True, allow_infinity=True))
def test_nan_handling(loss_value):
    if math.isnan(loss_value):
        with hypothesis.assume(True):
            result = optimizer_step_guard(loss_value)
            assert result == False, "Expected False for NaN loss_value"

@hypothesis.given(loss_value=st.floats(allow_nan=False, allow_infinity=False), max_loss=st.floats(allow_nan=False, allow_infinity=False))
def test_branch_specific_behavior(loss_value, max_loss):
    if loss_value == loss_value and loss_value > max_loss:
        with hypothesis.assume(True):
            result = optimizer_step_guard(loss_value, max_loss=max_loss)
            assert result == False, "Expected False when loss_value > max_loss"
    else:
        with hypothesis.assume(True):
            result = optimizer_step_guard(loss_value, max_loss=max_loss)
            assert result == True, "Expected True when loss_value <= max_loss"

@hypothesis.given(loss_value=st.floats(allow_nan=False, allow_infinity=False), max_loss=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition_false(loss_value, max_loss):
    if loss_value == loss_value and loss_value > max_loss:
        with hypothesis.assume(True):
            result = optimizer_step_guard(loss_value, max_loss=max_loss)
            assert result == False, "Expected False when loss_value > max_loss"

@hypothesis.given(loss_value=st.floats(allow_nan=False, allow_infinity=False), max_loss=st.floats(allow_nan=False, allow_infinity=False))
def test_return_postcondition_true(loss_value, max_loss):
    if not (loss_value == loss_value and loss_value > max_loss):
        with hypothesis.assume(True):
            result = optimizer_step_guard(loss_value, max_loss=max_loss)
            assert result == True, "Expected True when loss_value <= max_loss"