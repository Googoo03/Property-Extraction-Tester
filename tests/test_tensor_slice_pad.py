import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.tensor_slice_pad import tensor_slice_pad

@given(values=st.lists(st.integers()), start=st.integers(), end=st.integers())
def test_tensor_slice_pad_preserves_length(values, start, end):
    try:
        output = tensor_slice_pad(values, start, end)
        assert len(output) == len(values)
    except ValueError:
        pass

@given(values=st.lists(st.integers()), start=st.integers(), end=st.integers())
def test_tensor_slice_pad_invalid_range_raises_value_error(values, start, end):
    if start < 0 or end < start:
        with pytest.raises(ValueError):
            tensor_slice_pad(values, start, end)
    else:
        tensor_slice_pad(values, start, end)

@given(values=st.lists(st.integers()), start=st.integers(), end=st.integers())
def test_tensor_slice_pad_missing_non_negative_behavior(values, start, end):
    try:
        output = tensor_slice_pad(values, start, end)
        missing = end - start - len(values[start:end])
        if missing >= 0:
            assert len(output) == end - start
    except ValueError:
        pass

@given(values=st.lists(st.integers()), start=st.integers(), end=st.integers())
def test_tensor_slice_pad_return_postcondition(values, start, end):
    try:
        output = tensor_slice_pad(values, start, end)
        assert isinstance(output, list)
    except ValueError:
        pass