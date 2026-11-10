import math
import pytest
from valuation import run_dcf

def test_no_growth_equals_simple_perpetuity():
    # With no growth, $100 a year forever at a 10% return is worth $1000.
    value = run_dcf(fcf=100, shares=1, cash=0, debt=0, growth=0, terminal_growth=0, discount=0.1)
    assert math.isclose(value, 1000)

def test_cash_and_debt_change_value_per_share():
    base = run_dcf(fcf=100, shares =10, cash=0, debt=0, growth=0.05, terminal_growth=0.02, discount=0.09)
    adjusted = run_dcf(fcf=100, shares=10, cash=500, debt=200, growth=0.05, terminal_growth=0.02, discount=0.09)
    # $300 more net cash spread over 10 shares should increase value per share by $30.
    assert math.isclose(adjusted - base, 30)

def test_higher_discount_rate_means_lower_value():
    low_return = run_dcf(100, 1, 0, 0, growth=0.05, terminal_growth=0.02, discount=0.08)
    high_return = run_dcf(100, 1, 0, 0, growth=0.05, terminal_growth=0.02, discount=0.12)
    assert high_return < low_return

def test_negative_cash_flow_is_rejected():
    with pytest.raises(ValueError):
        run_dcf(fcf=-100, shares=1, cash=0, debt=0, growth=0.05, terminal_growth=0.02, discount=0.09)