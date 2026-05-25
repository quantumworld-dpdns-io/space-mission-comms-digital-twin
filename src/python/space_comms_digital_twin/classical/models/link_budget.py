from __future__ import annotations

import math
from dataclasses import dataclass

from space_comms_digital_twin.config import BOLTZMANN_CONSTANT, SPEED_OF_LIGHT


def friis_transmission_loss(distance: float, freq_hz: float) -> float:
    return (4.0 * math.pi * distance * freq_hz / SPEED_OF_LIGHT) ** 2


def calculate_eirp(tx_power_watts: float, tx_gain_linear: float) -> float:
    return tx_power_watts * tx_gain_linear


def calculate_snr(eirp: float, path_loss: float, rx_gain_linear: float,
                  noise_temp: float, bandwidth: float) -> float:
    rx_power = eirp * rx_gain_linear / path_loss
    noise_power = BOLTZMANN_CONSTANT * noise_temp * bandwidth
    return rx_power / noise_power


def calculate_eb_no(snr: float, bit_rate: float, bandwidth: float) -> float:
    return snr * bandwidth / bit_rate


def calculate_link_margin(received_power_dbw: float, sensitivity_dbw: float) -> float:
    return received_power_dbw - sensitivity_dbw


def calculate_space_loss(distance: float, freq_ghz: float) -> float:
    freq_hz = freq_ghz * 1e9
    return (4.0 * math.pi * distance * freq_hz / SPEED_OF_LIGHT) ** 2


def calculate_atmospheric_loss(freq_ghz: float, elevation_deg: float) -> float:
    freq = freq_ghz
    if elevation_deg < 5.0:
        return 10.0
    loss_per_km = 0.01 + 0.005 * (freq / 10.0)
    slant_path = 1.0 / math.sin(math.radians(elevation_deg))
    return loss_per_km * slant_path


def calculate_rain_attenuation(freq_ghz: float, rain_rate_mmh: float, elevation_deg: float) -> float:
    if rain_rate_mmh <= 0:
        return 0.0
    k = 0.01 * (freq_ghz ** 1.5)
    alpha = 1.5
    path_length = 1.0 / math.sin(math.radians(elevation_deg))
    return k * (rain_rate_mmh ** alpha) * path_length


def calculate_pointing_loss(angle_error_deg: float, beamwidth_deg: float) -> float:
    if beamwidth_deg <= 0:
        return 1.0
    ratio = angle_error_deg / (beamwidth_deg / 2.0)
    return 10.0 ** (-12.0 * (ratio ** 2) / 10.0)


def calculate_polarization_mismatch(tx_pol: str, rx_pol: str) -> float:
    if tx_pol == rx_pol:
        return 1.0
    if tx_pol.replace("linear_", "") == rx_pol.replace("linear_", ""):
        return 1.0
    return 0.5


def calculate_implementation_loss() -> float:
    return 2.0


def shannon_capacity_limit(bandwidth: float, snr: float) -> float:
    return bandwidth * math.log2(1.0 + snr)


def bandwidth_efficiency(modulation: str, coding_rate: float) -> float:
    mod_efficiency = {
        "BPSK": 1.0,
        "QPSK": 2.0,
        "8PSK": 3.0,
        "16QAM": 4.0,
        "64QAM": 6.0,
        "GMSK": 1.5,
    }
    return mod_efficiency.get(modulation.upper(), 1.0) * coding_rate


@dataclass
class LinkBudgetParams:
    tx_power_watts: float = 10.0
    tx_gain_dbi: float = 40.0
    rx_gain_dbi: float = 30.0
    frequency_ghz: float = 8.0
    distance_m: float = 1000000.0
    bandwidth_hz: float = 100e6
    rx_noise_temp_k: float = 290.0
    tx_polarization: str = "rhcp"
    rx_polarization: str = "rhcp"
    rain_rate_mmh: float = 0.0
    elevation_deg: float = 30.0
    modulation: str = "QPSK"
    coding_rate: float = 0.5
    rx_sensitivity_dbw: float = -120.0
    point_error_deg: float = 0.1


@dataclass
class LinkBudgetResult:
    eirp_dbw: float
    space_loss_db: float
    atmospheric_loss_db: float
    rain_loss_db: float
    pointing_loss_db: float
    polarization_loss_db: float
    total_path_loss_db: float
    rx_power_dbw: float
    noise_power_dbw: float
    snr_db: float
    eb_no_db: float
    link_margin_db: float
    shannon_capacity_bps: float
    spectral_efficiency_bps_hz: float


class LinkBudgetCalculator:
    def compute(self, params: LinkBudgetParams) -> LinkBudgetResult:
        tx_gain_linear = 10.0 ** (params.tx_gain_dbi / 10.0)
        rx_gain_linear = 10.0 ** (params.rx_gain_dbi / 10.0)

        eirp = calculate_eirp(params.tx_power_watts, tx_gain_linear)
        eirp_dbw = 10.0 * math.log10(eirp)

        space_loss = calculate_space_loss(params.distance_m, params.frequency_ghz)
        space_loss_db = 10.0 * math.log10(space_loss)

        atmospheric_loss_db = calculate_atmospheric_loss(params.frequency_ghz, params.elevation_deg)
        rain_loss_db = calculate_rain_attenuation(params.frequency_ghz, params.rain_rate_mmh, params.elevation_deg)
        pointing_loss = calculate_pointing_loss(params.point_error_deg, 1.0)
        pointing_loss_db = -10.0 * math.log10(max(pointing_loss, 1e-10))
        pol_mismatch = calculate_polarization_mismatch(params.tx_polarization, params.rx_polarization)
        polarization_loss_db = -10.0 * math.log10(max(pol_mismatch, 1e-10))

        total_loss = space_loss / (tx_gain_linear * rx_gain_linear * pointing_loss * pol_mismatch)
        total_loss_db = 10.0 * math.log10(total_loss)
        rx_power = eirp * rx_gain_linear * pointing_loss * pol_mismatch / space_loss
        rx_power_dbw = 10.0 * math.log10(max(rx_power, 1e-30))

        noise_power = BOLTZMANN_CONSTANT * params.rx_noise_temp_k * params.bandwidth_hz
        noise_power_dbw = 10.0 * math.log10(noise_power)

        snr = rx_power / noise_power
        snr_db = 10.0 * math.log10(max(snr, 1e-10))
        bit_rate = params.bandwidth_hz * bandwidth_efficiency(params.modulation, params.coding_rate)
        eb_no = calculate_eb_no(snr, bit_rate, params.bandwidth_hz)
        eb_no_db = 10.0 * math.log10(max(eb_no, 1e-10))
        link_margin = calculate_link_margin(rx_power_dbw, params.rx_sensitivity_dbw)
        shannon_cap = shannon_capacity_limit(params.bandwidth_hz, snr)

        return LinkBudgetResult(
            eirp_dbw=eirp_dbw,
            space_loss_db=space_loss_db,
            atmospheric_loss_db=atmospheric_loss_db,
            rain_loss_db=rain_loss_db,
            pointing_loss_db=pointing_loss_db,
            polarization_loss_db=polarization_loss_db,
            total_path_loss_db=total_loss_db,
            rx_power_dbw=rx_power_dbw,
            noise_power_dbw=noise_power_dbw,
            snr_db=snr_db,
            eb_no_db=eb_no_db,
            link_margin_db=link_margin,
            shannon_capacity_bps=shannon_cap,
            spectral_efficiency_bps_hz=bandwidth_efficiency(params.modulation, params.coding_rate),
        )
