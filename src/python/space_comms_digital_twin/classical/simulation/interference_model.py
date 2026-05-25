from __future__ import annotations

import math
from typing import Optional

import numpy as np


def adjacent_satellite_interference(d_theta_deg: float, pattern: str = "ideal", gain_max_dbi: float = 40.0) -> float:
    if pattern == "ideal":
        if abs(d_theta_deg) < 0.1:
            return 1.0
        return max(0.0, 1.0 - (abs(d_theta_deg) / 10.0))
    elif pattern == "sinc":
        x = math.pi * math.sin(math.radians(d_theta_deg)) / math.sin(math.radians(0.5))
        if abs(x) < 1e-10:
            return 1.0
        return (math.sin(x) / x) ** 2
    else:
        return 0.0


def pfd_computation(eirp_dbw: float, distance_m: float, bandwidth_hz: float) -> float:
    eirp_linear = 10.0 ** (eirp_dbw / 10.0)
    flux_density = eirp_linear / (4.0 * math.pi * distance_m ** 2)
    return 10.0 * math.log10(flux_density / bandwidth_hz)


def coordination_zone(satellite_power_dbm: float, interference_threshold_db: float = -10.0) -> float:
    return 10.0 ** ((satellite_power_dbm - interference_threshold_db) / 20.0)


def interference_to_noise_ratio(interference_power: float, noise_power: float) -> float:
    if noise_power <= 0:
        return float('inf')
    return interference_power / noise_power


def terrestrial_interference(terrestrial_eirp: float, rx_gain: float,
                             distance: float, frequency_ghz: float) -> float:
    from .link_budget import friis_transmission_loss
    wavelength = 299792458.0 / (frequency_ghz * 1e9)
    path_loss = (4.0 * math.pi * distance / wavelength) ** 2
    return terrestrial_eirp * rx_gain / path_loss
