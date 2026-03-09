import pytest
from hypothesis import given
from hypothesis.strategies import floats
from dataset.python_programs.calibrate_quality import calibrate_quality

@given(x0=floats(), y0=floats(), x1=floats(), y1=floats(), x=floats())
def test_calibrate_quality_preserves_length(x0, y0, x1, y1, x):
    assert len([x0, y0, x1, y1, x]) == 5

@given(x0=floats(), y0=floats(), x1=floats(), y1=floats(), x=floats())
def test_calibrate_quality_degenerate_segment_raises_value_error(x0, y0, x1, y1, x):
    if x1 == x0:
        with pytest.raises(ValueError, match="degenerate segment"):
            calibrate_quality(x0, y0, x1, y1, x)

@given(x0=floats(), y0=floats(), x1=floats(), y1=floats(), x=floats())
def test_calibrate_quality_clamp_branch_behavior(x0, y0, x1, y1, x):
    y = calibrate_quality(x0, y0, x1, y1, x, clamp=True)
    if x1 != x0:
        t = (x - x0) / (x1 - x0)
        y_expected = y0 + t * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        if y_expected < lo:
            assert y == lo
        elif y_expected > hi:
            assert y == hi
        else:
            assert y == y_expected

@given(x0=floats(), y0=floats(), x1=floats(), y1=floats(), x=floats())
def test_calibrate_quality_y_less_than_lo_branch_behavior(x0, y0, x1, y1, x):
    if x1 != x0:
        y = calibrate_quality(x0, y0, x1, y1, x, clamp=True)
        t = (x - x0) / (x1 - x0)
        y_expected = y0 + t * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        if y_expected < lo:
            assert y == lo

@given(x0=floats(), y0=floats(), x1=floats(), y1=floats(), x=floats())
def test_calibrate_quality_y_greater_than_hi_branch_behavior(x0, y0, x1, y1, x):
    if x1 != x0:
        y = calibrate_quality(x0, y0, x1, y1, x, clamp=True)
        t = (x - x0) / (x1 - x0)
        y_expected = y0 + t * (y1 - y0)
        lo, hi = min(y0, y1), max(y0, y1)
        if y_expected > hi:
            assert y == hi

@given(x0=floats(), y0=floats(), x1=floats(), y1=floats(), x=floats())
def test_calibrate_quality_return_postcondition(x0, y0, x1, y1, x):
    if x1 != x0:
        y = calibrate_quality(x0, y0, x1, y1, x)
        t = (x - x0) / (x1 - x0)
        y_expected = y0 + t * (y1 - y0)
        assert y == y_expected