from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class Antenna:
    id: str
    name: str
    diameter: float
    frequency_ghz: float
    gain_dbi: float
    beamwidth_deg: float
    polarization: str = "rhcp"
    pointing_mode: str = "az_el"
    max_power_watts: float = 100.0
    noise_temperature: float = 290.0
    efficiency: float = 0.65

    def compute_gain(self, theta_deg: float, phi_deg: float) -> float:
        hp = self.beamwidth_deg
        theta_norm = theta_deg / (hp / 2.0)
        if abs(theta_norm) > 2.0:
            return -30.0
        pattern = -12.0 * (theta_norm ** 2)
        return self.gain_dbi + pattern

    def compute_eirp(self, power_watts: float) -> float:
        gain_linear = 10.0 ** (self.gain_dbi / 10.0)
        return power_watts * gain_linear

    def compute_half_power_beamwidth(self) -> float:
        wavelength = 299792458.0 / (self.frequency_ghz * 1e9)
        return 70.0 * wavelength / self.diameter

    def pointing_error_deg(self, target_az: float, target_el: float,
                           actual_az: float, actual_el: float) -> float:
        return math.sqrt((target_az - actual_az) ** 2 + (target_el - actual_el) ** 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "frequency_ghz": self.frequency_ghz,
            "gain_dbi": self.gain_dbi,
            "beamwidth_deg": self.beamwidth_deg,
            "polarization": self.polarization,
            "pointing_mode": self.pointing_mode,
            "max_power_watts": self.max_power_watts,
            "noise_temperature": self.noise_temperature,
        }

    def __repr__(self) -> str:
        return f"Antenna(id='{self.id}', name='{self.name}', gain={self.gain_dbi}dBi)"
