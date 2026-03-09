import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.retry_backoff_window import retry_backoff_window

@given(attempts=st.integers(min_value=0, max_value=10), base=st.integers(min_value=1, max_value=10), max_delay=st.integers(min_value=1, max_value=100))
def test_retry_backoff_window_basic(attempts, base, max_delay):
    delay = retry_backoff_window(attempts, base=base, max_delay=max_delay)
    assert isinstance(delay, int)
    assert delay >= 0

@given(attempts=st.integers(max_value=-1))
def test_retry_backoff_window_negative_attempts_raises_value_error(attempts):
    with pytest.raises(ValueError):
        retry_backoff_window(attempts)

@given(attempts=st.integers(min_value=0), base=st.integers(min_value=1), max_delay=st.integers(min_value=1))
def test_retry_backoff_window_delay_not_exceeding_max(attempts, base, max_delay):
    delay = retry_backoff_window(attempts, base=base, max_delay=max_delay)
    assert delay <= max_delay

@given(attempts=st.integers(min_value=0), base=st.integers(min_value=1), max_delay=st.integers(min_value=1))
def test_retry_backoff_window_correct_exponential_calculation(attempts, base, max_delay):
    expected_delay = base * (2 ** attempts)
    actual_delay = retry_backoff_window(attempts, base=base, max_delay=max_delay)
    if expected_delay <= max_delay:
        assert actual_delay == expected_delay
    else:
        assert actual_delay == max_delay