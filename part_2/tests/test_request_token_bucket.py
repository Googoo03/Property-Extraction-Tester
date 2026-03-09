import hypothesis
from hypothesis import strategies as st
from hypothesis import given, example
from dataset.python_programs.request_token_bucket import request_token_bucket

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 10, 'last': 0}, now=0, rate=1, capacity=10)
def test_preserves_length(tokens, now, rate, capacity):
    try:
        output = request_token_bucket(tokens, now, rate=rate, capacity=capacity)
        assert isinstance(output, bool)
    except ValueError:
        pass

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 10, 'last': 0}, now=0, rate=-1, capacity=10)
@example(tokens={'available': 10, 'last': 0}, now=0, rate=1, capacity=-10)
def test_branch_specific_behavior_rate_or_capacity_invalid(tokens, now, rate, capacity):
    try:
        request_token_bucket(tokens, now, rate=rate, capacity=capacity)
        assert False  # Should not reach here if ValueError is raised
    except ValueError:
        pass

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 0, 'last': 0}, now=0, rate=1, capacity=10)
def test_branch_specific_behavior_available_non_positive(tokens, now, rate, capacity):
    try:
        output = request_token_bucket(tokens, now, rate=rate, capacity=capacity)
        assert output is False
    except ValueError:
        pass

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 0, 'last': 0}, now=0, rate=1, capacity=10)
def test_return_postcondition_false(tokens, now, rate, capacity):
    try:
        output = request_token_bucket(tokens, now, rate=rate, capacity=capacity)
        if tokens.get('available', capacity) <= 0:
            assert output is False
    except ValueError:
        pass

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 1, 'last': 0}, now=1, rate=1, capacity=10)
def test_return_postcondition_true(tokens, now, rate, capacity):
    try:
        output = request_token_bucket(tokens, now, rate=rate, capacity=capacity)
        if tokens.get('available', capacity) > 0:
            assert output is True
    except ValueError:
        pass

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 1, 'last': 0}, now=1, rate=1, capacity=10)
def test_updates_last(tokens, now, rate, capacity):
    try:
        tokens_copy = tokens.copy()
        request_token_bucket(tokens, now, rate=rate, capacity=capacity)
        if tokens.get('available', capacity) > 0:
            assert tokens['last'] == now
        else:
            assert tokens['last'] == tokens_copy.get('last', now)
    except ValueError:
        pass

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 1, 'last': 0}, now=1, rate=1, capacity=10)
def test_updates_available(tokens, now, rate, capacity):
    try:
        tokens_copy = tokens.copy()
        available = tokens_copy.get('available', capacity)
        last = tokens_copy.get('last', now)
        refill = int((now - last) * rate)
        expected_available = min(capacity, available + refill) - 1
        request_token_bucket(tokens, now, rate=rate, capacity=capacity)
        if tokens.get('available', capacity) > 0:
            assert tokens['available'] == expected_available
        else:
            assert tokens['available'] == available
    except ValueError:
        pass

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 1, 'last': 0}, now=1, rate=1, capacity=10)
def test_updates_last_when_token_consumed(tokens, now, rate, capacity):
    try:
        tokens_copy = tokens.copy()
        available = tokens_copy.get('available', capacity)
        if available > 0:
            request_token_bucket(tokens, now, rate=rate, capacity=capacity)
            assert tokens['last'] == now
        else:
            request_token_bucket(tokens, now, rate=rate, capacity=capacity)
            assert tokens['last'] == tokens_copy.get('last', now)
    except ValueError:
        pass

@given(tokens=st.dictionaries(st.text(), st.integers()), now=st.integers(), rate=st.integers(), capacity=st.integers())
@example(tokens={'available': 0, 'last': 0}, now=0, rate=1, capacity=10)
def test_does_not_update_last_when_no_token_consumed(tokens, now, rate, capacity):
    try:
        tokens_copy = tokens.copy()
        available = tokens_copy.get('available', capacity)
        if available <= 0:
            request_token_bucket(tokens, now, rate=rate, capacity=capacity)
            assert tokens['last'] == tokens_copy.get('last', now)
        else:
            request_token_bucket(tokens, now, rate=rate, capacity=capacity)
            assert tokens['last'] == now
    except ValueError:
        pass