import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.gpu_memory_pool import gpu_memory_pool

@given(allocations=st.lists(st.integers(min_value=0), min_size=0),
       request=st.integers(min_value=0),
       capacity=st.integers(min_value=1))
def test_gpu_memory_pool_positive_capacity(allocations, request, capacity):
    assert gpu_memory_pool(allocations, request, capacity=capacity) is True

@given(allocations=st.lists(st.integers(min_value=0), min_size=0),
       request=st.integers(min_value=0))
def test_gpu_memory_pool_zero_capacity_raises_error(allocations, request):
    with pytest.raises(ValueError):
        gpu_memory_pool(allocations, request, capacity=0)

@given(allocations=st.lists(st.integers(min_value=0), min_size=0),
       request=st.integers(max_value=-1),
       capacity=st.integers(min_value=1))
def test_gpu_memory_pool_negative_request_raises_error(allocations, request, capacity):
    with pytest.raises(ValueError):
        gpu_memory_pool(allocations, request, capacity=capacity)

@given(allocations=st.lists(st.integers(min_value=0), min_size=0),
       request=st.integers(min_value=0),
       capacity=st.integers(min_value=1))
def test_gpu_memory_pool_exceeds_capacity_returns_false(allocations, request, capacity):
    total_used = sum(allocations)
    if total_used + request > capacity:
        assert gpu_memory_pool(allocations, request, capacity=capacity) is False

@given(allocations=st.lists(st.integers(min_value=0), min_size=0),
       request=st.integers(min_value=0),
       capacity=st.integers(min_value=1))
def test_gpu_memory_pool_within_capacity_returns_true(allocations, request, capacity):
    total_used = sum(allocations)
    if total_used + request <= capacity:
        assert gpu_memory_pool(allocations, request, capacity=capacity) is True