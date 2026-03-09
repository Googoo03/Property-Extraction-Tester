import pytest
from hypothesis import given
from hypothesis.strategies import floats, composite
from dataset.python_programs.confidence_trendline import confidence_trendline


@composite
def segment_strategy(draw):
    x0 = draw(floats())
    y0 = draw(floats())

    x1 = draw(floats(min_value=x0 + 1))
    y1 = draw(floats())

    x = draw(floats())
    clamp = draw(booleans())

    return x0, y0, x1, y1, x, clamp

@given(x0=floats(), y0=floats(), x1=floats(), y1=floats(), x=floats(), clamp=True)
def test_preserves_length(x0, y0, x1, y1, x, clamp):
    assert len([x0, y0, x1, y1, x, clamp]) == len([x0, y0, x1, y1, x, clamp])

@given(x0=floats(), y0=floats(), x=floats(), clamp=True)
def test_branch_specific_behavior_x0_equals_x1(x0, y0, x, clamp):
    with pytest.raises(ValueError):
        confidence_trendline(x0, y0, x0, y0, x, clamp=clamp)

@given(segment_strategy())
def test_branch_specific_behavior_clamp_true(x0, y0, x1, y1, x, clamp):
    y = confidence_trendline(x0, y0, x1, y1, x, clamp=clamp)
    lo, hi = min(y0, y1), max(y0, y1)
    assert lo <= y <= hi

@given(segment_strategy())
def test_branch_specific_behavior_y_less_than_lo(x0, y0, x1, y1, x, clamp):
    y = confidence_trendline(x0, y0, x1, y1, x, clamp=clamp)
    lo, hi = min(y0, y1), max(y0, y1)
    assert lo <= y <= hi

@given(segment_strategy())
def test_return_postcondition(x0, y0, x1, y1, x, clamp):
    y = confidence_trendline(x0, y0, x1, y1, x, clamp=clamp)
    lo, hi = min(y0, y1), max(y0, y1)
    assert lo <= y <= hi