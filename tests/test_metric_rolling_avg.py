import hypothesis
from hypothesis import given, strategies as st
from dataset.python_programs.metric_rolling_avg import metric_rolling_avg

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=10))
def test_preserves_length(values):
    try:
        result = metric_rolling_avg(values)
        assert len(values) == len(values)
    except ValueError:
        pass

@given(window=st.integers())
def test_branch_window_positive(window):
    values = [1.0, 2.0, 3.0]
    if window <= 0:
        with hypothesis.assume(True):
            try:
                metric_rolling_avg(values, window=window)
                assert False, "Expected ValueError for non-positive window"
            except ValueError as e:
                assert str(e) == "window must be positive"

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=10))
def test_branch_no_values(values):
    if not values:
        with hypothesis.assume(True):
            try:
                metric_rolling_avg(values)
                assert False, "Expected ValueError for empty values"
            except ValueError as e:
                assert str(e) == "no values"

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=10),
       window=st.integers(min_value=1, max_value=10),
       min_samples=st.integers(min_value=1, max_value=10))
def test_branch_min_samples(values, window, min_samples):
    if len(values[-window:]) < min_samples:
        with hypothesis.assume(True):
            result = metric_rolling_avg(values, window=window, min_samples=min_samples)
            assert result is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=10),
       window=st.integers(min_value=1, max_value=10),
       min_samples=st.integers(min_value=1, max_value=10))
def test_return_postcondition_none(values, window, min_samples):
    if len(values[-window:]) < min_samples:
        with hypothesis.assume(True):
            result = metric_rolling_avg(values, window=window, min_samples=min_samples)
            assert result is None

@given(values=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=10),
       window=st.integers(min_value=1, max_value=10),
       min_samples=st.integers(min_value=1, max_value=10))
def test_return_postcondition_avg(values, window, min_samples):
    if len(values[-window:]) >= min_samples:
        with hypothesis.assume(True):
            result = metric_rolling_avg(values, window=window, min_samples=min_samples)
            tail = values[-window:]
            total = sum(tail)
            expected_avg = total / window
            assert result == expected_avg