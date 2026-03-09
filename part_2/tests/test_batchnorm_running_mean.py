import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.batchnorm_running_mean import batchnorm_running_mean

@given(current_mean=st.floats(), batch_mean=st.floats(), momentum=st.floats())
def test_momentum_range(current_mean, batch_mean, momentum):
    if not (0 <= momentum <= 1):
        with pytest.raises(ValueError):
            batchnorm_running_mean(current_mean, batch_mean, momentum=momentum)

@given(current_mean=st.floats(), batch_mean=st.floats(), momentum=st.floats())
def test_current_mean_type(current_mean, batch_mean, momentum):
    if not (0 <= momentum <= 1):
        with pytest.raises(ValueError):
            batchnorm_running_mean(current_mean, batch_mean, momentum=momentum)

@given(current_mean=st.floats(), batch_mean=st.floats(), momentum=st.floats())
def test_batch_mean_type(current_mean, batch_mean, momentum):
    if not (0 <= momentum <= 1):
        with pytest.raises(ValueError):
            batchnorm_running_mean(current_mean, batch_mean, momentum=momentum)

@given(current_mean=st.floats(), batch_mean=st.floats(), momentum=st.floats())
def test_length_consistency(current_mean, batch_mean, momentum):
    if isinstance(current_mean, (list, tuple)) and isinstance(batch_mean, (list, tuple)):
        if len(current_mean) != len(batch_mean):
            with pytest.raises(ValueError):
                batchnorm_running_mean(current_mean, batch_mean, momentum=momentum)

@given(current_mean=st.floats(), batch_mean=st.floats(), momentum=st.floats())
def test_return_postcondition(current_mean, batch_mean, momentum):
    if 0 <= momentum <= 1:
        expected = (1 - momentum) * current_mean + momentum * batch_mean
        assert batchnorm_running_mean(current_mean, batch_mean, momentum=momentum) == expected

@given(current_mean=st.floats(), batch_mean=st.floats(), momentum=st.floats())
def test_branch_specific_behavior(current_mean, batch_mean, momentum):
    if not (0 <= momentum <= 1):
        with pytest.raises(ValueError):
            batchnorm_running_mean(current_mean, batch_mean, momentum=momentum)
    else:
        assert batchnorm_running_mean(current_mean, batch_mean, momentum=momentum) == (1 - momentum) * current_mean + momentum * batch_mean