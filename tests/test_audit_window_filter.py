import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.audit_window_filter import audit_window_filter

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers())
def test_audit_window_filter_preserves_length(timestamps, now, window):
    cutoff = now - window
    output = audit_window_filter(timestamps, now, window=window)
    assert len(output) <= len(timestamps)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers())
def test_audit_window_filter_return_postcondition(timestamps, now, window):
    cutoff = now - window
    output = audit_window_filter(timestamps, now, window=window)
    assert all(t >= cutoff for t in output)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers())
def test_audit_window_filter_loop_invariant(timestamps, now, window):
    cutoff = now - window
    output = audit_window_filter(timestamps, now, window=window)
    assert all(t in output for t in timestamps if t >= cutoff)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers())
def test_audit_window_filter_boundary_inclusion(timestamps, now, window):
    cutoff = now - window
    output = audit_window_filter(timestamps, now, window=window)
    assert all(t in output for t in timestamps if t == cutoff)

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers())
def test_audit_window_filter_non_negative_window(timestamps, now, window):
    assert window >= 0

@given(timestamps=st.lists(st.integers()), now=st.integers(), window=st.integers())
def test_audit_window_filter_output_subset(timestamps, now, window):
    output = audit_window_filter(timestamps, now, window=window)
    assert set(output).issubset(set(timestamps))