import math
import pytest
from space_comms_digital_twin.classical.models.link_budget import (
    LinkBudgetCalculator,
    LinkBudgetParams,
    friis_transmission_loss,
    calculate_snr,
    calculate_link_margin,
)


def test_friis_transmission():
    loss = friis_transmission_loss(1e6, 8e9)
    assert loss > 0
    assert math.isfinite(loss)


def test_link_budget_calculator():
    calc = LinkBudgetCalculator()
    params = LinkBudgetParams(distance_m=1e6, frequency_ghz=8.0)
    result = calc.compute(params)
    assert result.snr_db != 0
    assert result.link_margin_db != 0
    assert result.eirp_dbw > 0


def test_link_margin_positive():
    margin = calculate_link_margin(-100, -120)
    assert margin == 20.0


def test_snr_ratio():
    snr = calculate_snr(1000, 1e12, 1000, 290, 100e6)
    assert snr > 0
