from __future__ import annotations

import math
from typing import List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

from space_comms_digital_twin.config import EARTH_RADIUS


def check_horizon_elevation(sat_az_el: Tuple[float, float, float], station_mask_deg: float) -> bool:
    _, el, _ = sat_az_el
    return el >= station_mask_deg


def elevation_angle(sat_pos: NDArray, station_pos: NDArray) -> float:
    los = sat_pos - station_pos
    r_los = np.linalg.norm(los)
    r_sat = np.linalg.norm(sat_pos)
    r_station = np.linalg.norm(station_pos)
    cos_zenith = np.dot(los, station_pos) / (r_los * r_station)
    zenith = math.acos(max(-1.0, min(1.0, cos_zenith)))
    return math.degrees(math.pi / 2.0 - zenith)


def range_to_satellite(sat_pos: NDArray, station_pos: NDArray) -> float:
    return float(np.linalg.norm(sat_pos - station_pos))


def compute_range_rate(sat_vel: NDArray, station_pos: NDArray, sat_pos: NDArray) -> float:
    los = sat_pos - station_pos
    r_los = np.linalg.norm(los)
    if r_los < 1e-6:
        return 0.0
    return float(np.dot(sat_vel, los) / r_los)


def contact_window(satellite, station, start_time, end_time, time_step: float = 10.0) -> List[dict]:
    windows = []
    current_time = start_time
    in_contact = False
    contact_start = None
    contacts = []

    while current_time <= end_time:
        try:
            sat_pos = satellite.get_position_eci(current_time)
        except Exception:
            current_time += time_step
            continue

        try:
            az_el_range = station.get_az_el_range(sat_pos, current_time)
        except Exception:
            current_time += time_step
            continue

        _, el, rng = az_el_range
        visible = el >= station.elevation_mask

        if visible and not in_contact:
            in_contact = True
            contact_start = current_time
        elif not visible and in_contact:
            in_contact = False
            windows.append({
                "start": contact_start,
                "end": current_time,
                "duration": (current_time - contact_start).total_seconds(),
                "max_elevation": 0.0,
                "min_range": float('inf'),
            })
            contact_start = None

        current_time += time_step

    if in_contact:
        windows.append({
            "start": contact_start,
            "end": end_time,
            "duration": (end_time - contact_start).total_seconds(),
            "max_elevation": 0.0,
            "min_range": float('inf'),
        })

    return windows


def multi_site_visibility(satellite, stations: list, time: object) -> List[dict]:
    results = []
    sat_pos = satellite.get_position_eci(time)
    for station in stations:
        az, el, rng = station.get_az_el_range(sat_pos, time)
        results.append({
            "station_id": station.id,
            "station_name": station.name,
            "azimuth": az,
            "elevation": el,
            "range": rng,
            "visible": el >= station.elevation_mask,
        })
    return results


def handover_prediction(satellites: list, stations: list, times: List[object]) -> List[dict]:
    schedule = []
    for t in times:
        best_el = -90.0
        best_pair = None
        for sat in satellites:
            sat_pos = sat.get_position_eci(t)
            for station in stations:
                _, el, _ = station.get_az_el_range(sat_pos, t)
                if el > best_el:
                    best_el = el
                    best_pair = (sat.norad_id, station.id)
        if best_pair and best_el > 0:
            schedule.append({
                "time": t,
                "satellite_id": best_pair[0],
                "station_id": best_pair[1],
                "elevation": best_el,
            })
    return schedule


def coverage_map(satellites: list, lat_grid: NDArray, lon_grid: NDArray, time: object) -> NDArray:
    coverage = np.zeros((len(lat_grid), len(lon_grid)), dtype=bool)
    for i, lat in enumerate(lat_grid):
        for j, lon in enumerate(lon_grid):
            for sat in satellites:
                try:
                    sat_pos = sat.get_position_eci(time)
                    az, el, rng = 0.0, 0.0, 0.0
                    r_sat = np.linalg.norm(sat_pos)
                    if r_sat == 0:
                        continue
                    el = math.degrees(math.asin(abs(sat_pos[2]) / r_sat))
                    if el > 5.0:
                        coverage[i, j] = True
                        break
                except Exception:
                    continue
    return coverage


def doppler_rate(freq_hz: float, range_rate: float) -> float:
    return freq_hz * range_rate / 299792458.0
