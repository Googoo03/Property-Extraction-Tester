import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.throughput_trendline import throughput_trendline

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_preserve_length(x0, y0, x1, y1, x):
    assert isinstance(throughput_trendline(x0, y0, x1, y1, x), float)

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_branch_specific_behavior_zero_length(x0, y0, x1, y1, x):
    with pytest.raises(ValueError, match="zero length"):
        throughput_trendline(x0, y0, x0, y1, x)

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_branch_specific_behavior_clamp_true(x0, y0, x1, y1, x):
    result = throughput_trendline(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert low <= result <= high

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_branch_specific_behavior_clamp_false(x0, y0, x1, y1, x):
    result = throughput_trendline(x0, y0, x1, y1, x, clamp=False)
    t = (x - x0) / (x1 - x0)
    expected = (1 - t) * y0 + t * y1
    assert result == expected

@given(
    x0=st.floats(allow_nan=False, allow_infinity=False),
    y0=st.floats(allow_nan=False, allow_infinity=False),
    x1=st.floats(allow_nan=False, allow_infinity=False),
    y1=st.floats(allow_nan=False, allow_infinity=False),
    x=st.floats(allow_nan=False, allow_infinity=False)
)
def test_return_postcondition(x0, y0, x1, y1, x):
    result = throughput_trendline(x0, y0, x1, y1, x)
    t = (x - x0) / (x1 - x0)
    expected = (1 - t) * y0 + t * y1
    assert result == expected