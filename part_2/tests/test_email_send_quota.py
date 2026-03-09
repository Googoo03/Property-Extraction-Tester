from hypothesis import given
from hypothesis import strategies as st
from datetime import datetime, timedelta
import pytest

from dataset.python_programs.email_send_quota import email_send_quota

@given(
    sent=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_preserves_length(sent, now, window, limit):
    cutoff = now - window
    recent = [t for t in sent if t >= cutoff]
    output = email_send_quota(sent, now, window=window, limit=limit)
    assert len(recent) <= len(sent)

@given(
    sent=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_loop_invariant(sent, now, window, limit):
    cutoff = now - window
    recent = [t for t in sent if t >= cutoff]
    output = email_send_quota(sent, now, window=window, limit=limit)
    assert all(t >= cutoff for t in recent)

@given(
    sent=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_branch_specific_behavior(sent, now, window, limit):
    cutoff = now - window
    recent = [t for t in sent if t >= cutoff]
    output = email_send_quota(sent, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == False
    else:
        assert output == True

@given(
    sent=st.lists(st.integers(min_value=0)),
    now=st.integers(min_value=0),
    window=st.integers(min_value=1),
    limit=st.integers(min_value=1)
)
def test_return_postcondition(sent, now, window, limit):
    cutoff = now - window
    recent = [t for t in sent if t >= cutoff]
    output = email_send_quota(sent, now, window=window, limit=limit)
    if len(recent) > limit:
        assert output == False
    else:
        assert output == True