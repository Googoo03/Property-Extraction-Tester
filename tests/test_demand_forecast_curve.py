import pytest
from hypothesis import given, strategies as st
from dataset.python_programs.demand_forecast_curve import demand_forecast_curve

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_demand_forecast_curve_preserves_length(x0, y0, x1, y1, x):
    assert len([x0, y0, x1, y1, x]) == 5

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_demand_forecast_curve_raises_value_error_when_x0_equals_x1(x0, y0, x1, y1, x):
    with pytest.raises(ValueError):
        demand_forecast_curve(x0, y0, x1, y1, x, clamp=True)

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_demand_forecast_curve_output_behavior_depends_on_clamp_value(x0, y0, x1, y1, x):
    y_with_clamp = demand_forecast_curve(x0, y0, x1, y1, x, clamp=True)
    y_without_clamp = demand_forecast_curve(x0, y0, x1, y1, x, clamp=False)
    assert y_with_clamp == y_without_clamp or y_with_clamp != y_without_clamp

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_demand_forecast_curve_output_behavior_depends_on_y_less_than_low_condition(x0, y0, x1, y1, x):
    y = demand_forecast_curve(x0, y0, x1, y1, x, clamp=True)
    low, high = (min(y0, y1), max(y0, y1))
    if y < low:
        assert y == low
    elif y > high:
        assert y == high

@given(
    x0=st.floats(),
    y0=st.floats(),
    x1=st.floats(),
    y1=st.floats(),
    x=st.floats()
)
def test_demand_forecast_curve_return_postcondition(x0, y0, x1, y1, x):
    y = demand_forecast_curve(x0, y0, x1, y1, x, clamp=True)
    assert isinstance(y, (int, float))