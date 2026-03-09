import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.search_result_pager import search_result_pager

@given(results=st.lists(st.integers()), page=st.integers(min_value=1), page_size=st.integers(min_value=1))
def test_preserves_length(results, page, page_size):
    output = search_result_pager(results, page, page_size=page_size)
    assert len(output) == len(results)

@given(page=st.integers(max_value=0))
def test_branch_specific_behavior_page_less_than_one(page):
    with pytest.raises(ValueError, match="page must be >= 1"):
        search_result_pager([], page)

@given(page_size=st.integers(max_value=0))
def test_branch_specific_behavior_page_size_less_than_or_equal_zero(page_size):
    with pytest.raises(ValueError, match="page_size must be positive"):
        search_result_pager([], 1, page_size=page_size)

@given(results=st.lists(st.integers()), page=st.integers(min_value=1), page_size=st.integers(min_value=1))
def test_return_postcondition(results, page, page_size):
    start = (page - 1) * page_size
    end = start + page_size
    expected = results[start:end + 1]
    output = search_result_pager(results, page, page_size=page_size)
    assert output == expected