from __future__ import annotations

import math
from typing import Callable, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

from space_comms_digital_twin.config import EARTH_MU, EARTH_RADIUS, EARTH_ROTATION_RATE


def kepler_propagate(elements: dict, delta_t: float) -> dict:
    n = elements["mean_motion"] * 2.0 * math.pi / 86400.0
    M = math.radians(elements["mean_anomaly"]) + n * delta_t
    E = _solve_kepler(M, elements["eccentricity"])
    new_anomaly = math.degrees(E % (2.0 * math.pi))
    new_elements = dict(elements)
    new_elements["mean_anomaly"] = new_anomaly
    return new_elements


def _solve_kepler(M: float, e: float, tol: float = 1e-10, max_iter: int = 100) -> float:
    E = M if e < 0.8 else math.pi
    for _ in range(max_iter):
        dE = (M - E + e * math.sin(E)) / (1.0 - e * math.cos(E))
        E += dE
        if abs(dE) < tol:
            break
    return E


def sgp4_propagate(tle_line1: str, tle_line2: str, epoch: object) -> Tuple[NDArray, NDArray]:
    from sgp4.api import Satrec, jday
    sat = Satrec.twoline2rv(tle_line1, tle_line2)
    jd, fr = jday(
        epoch.year, epoch.month, epoch.day,
        epoch.hour, epoch.minute,
        epoch.second + epoch.microsecond / 1e6,
    )
    err, pos, vel = sat.sgp4(jd, fr)
    if err != 0:
        raise RuntimeError(f"SGP4 error code: {err}")
    return np.array(pos) * 1000.0, np.array(vel) * 1000.0


def rk4_integrate(initial_state: NDArray, dt: float, n_steps: int,
                  deriv_func: Callable) -> NDArray:
    state = initial_state.copy()
    for _ in range(n_steps):
        k1 = deriv_func(state)
        k2 = deriv_func(state + 0.5 * dt * k1)
        k3 = deriv_func(state + 0.5 * dt * k2)
        k4 = deriv_func(state + dt * k3)
        state += (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return state


def eci_to_ecef(eci_pos: NDArray, gmst: float) -> NDArray:
    c, s = math.cos(gmst), math.sin(gmst)
    rot = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
    return rot @ eci_pos


def ecef_to_lla(ecef_pos: NDArray) -> Tuple[float, float, float]:
    x, y, z = ecef_pos
    lon = math.degrees(math.atan2(y, x))
    p = math.sqrt(x ** 2 + y ** 2)
    lat = math.degrees(math.atan2(z, p))
    alt = math.sqrt(x ** 2 + y ** 2 + z ** 2) - EARTH_RADIUS
    return lat, lon, alt


def lla_to_ecef(lat_deg: float, lon_deg: float, alt_m: float) -> NDArray:
    lat_r = math.radians(lat_deg)
    lon_r = math.radians(lon_deg)
    r = EARTH_RADIUS + alt_m
    return np.array([
        r * math.cos(lat_r) * math.cos(lon_r),
        r * math.cos(lat_r) * math.sin(lon_r),
        r * math.sin(lat_r),
    ])


def eci_to_topo(eci_pos: NDArray, observer_ecef: NDArray, gmst: float) -> Tuple[float, float, float]:
    ecef = eci_to_ecef(eci_pos, gmst)
    los = ecef - observer_ecef
    r = np.linalg.norm(los)
    return 0.0, 0.0, r


def compute_gmst(julian_date: float) -> float:
    t = (julian_date - 2451545.0) / 36525.0
    gmst = 280.46061837 + 360.98564736629 * (julian_date - 2451545.0) + 0.000387933 * t ** 2 - (t ** 3) / 38710000.0
    return math.radians(gmst % 360.0)


def compute_orbit_elements_from_state(r_vec: NDArray, v_vec: NDArray) -> dict:
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    h_vec = np.cross(r_vec, v_vec)
    h = np.linalg.norm(h_vec)

    n_vec = np.cross([0, 0, 1], h_vec)
    n = np.linalg.norm(n_vec)

    e_vec = (np.cross(v_vec, h_vec) / EARTH_MU) - (r_vec / r)
    e = np.linalg.norm(e_vec)

    energy = v ** 2 / 2.0 - EARTH_MU / r
    a = -EARTH_MU / (2.0 * energy)

    i = math.degrees(math.acos(h_vec[2] / h))
    raan = math.degrees(math.atan2(n_vec[1], n_vec[0])) if n > 0 else 0.0
    arg_p = math.degrees(math.acos(np.dot(n_vec, e_vec) / (n * e))) if n > 0 and e > 0 else 0.0
    nu = math.degrees(math.acos(np.dot(e_vec, r_vec) / (e * r))) if e > 0 else 0.0

    return {
        "semi_major_axis": a,
        "eccentricity": e,
        "inclination": i,
        "raan": raan,
        "arg_perigee": arg_p,
        "true_anomaly": nu,
    }


def ground_track_coordinates(elements: dict, times: NDArray) -> NDArray:
    coords = []
    for t in times:
        new_el = kepler_propagate(elements, t)
        a = new_el.get("semi_major_axis", elements.get("semi_major_axis", EARTH_RADIUS + 400000))
        e = new_el["eccentricity"]
        i = math.radians(new_el["inclination"])
        raan = math.radians(new_el.get("raan", 0))
        arg_p = math.radians(new_el.get("arg_perigee", 0))
        E = _solve_kepler(math.radians(new_el.get("mean_anomaly", 0)), e)
        x = a * (math.cos(E) - e)
        y = a * math.sqrt(1 - e ** 2) * math.sin(E)
        r = math.sqrt(x ** 2 + y ** 2)
        nu = math.atan2(y, x)

        pos_eci = np.array([
            r * (math.cos(raan) * math.cos(arg_p + nu) - math.sin(raan) * math.sin(arg_p + nu) * math.cos(i)),
            r * (math.sin(raan) * math.cos(arg_p + nu) + math.cos(raan) * math.sin(arg_p + nu) * math.cos(i)),
            r * math.sin(arg_p + nu) * math.sin(i),
        ])
        gmst = compute_gmst(2451545.0 + t / 86400.0)
        lat, lon, _ = ecef_to_lla(eci_to_ecef(pos_eci, gmst))
        coords.append([lon, lat, t])
    return np.array(coords)


def compute_eclipse(sat_pos: NDArray, sun_pos: NDArray) -> bool:
    norm_pos = np.linalg.norm(sat_pos)
    norm_sun = np.linalg.norm(sun_pos)
    if np.dot(sat_pos, sun_pos) / (norm_pos * norm_sun) > 0:
        return False
    shadow_angle = math.asin(EARTH_RADIUS / norm_pos)
    sun_angle = math.acos(np.dot(sat_pos, sun_pos) / (norm_pos * norm_sun))
    return sun_angle < shadow_angle


def sun_vector_at_time(epoch: object) -> NDArray:
    from astropy.time import Time
    from astropy.coordinates import get_sun
    t = Time(epoch)
    sun = get_sun(t)
    cart = sun.represent_as('cartesian')
    return np.array([cart.x.value, cart.y.value, cart.z.value])


def doppler_shift(freq_hz: float, relative_velocity_ms: float) -> float:
    return freq_hz * (1.0 + relative_velocity_ms / 299792458.0)


def multi_satellite_propagation(satellites: list, times: NDArray) -> NDArray:
    positions = []
    for sat in satellites:
        sat_positions = []
        for t in times:
            pos = sat.get_position_eci()
            sat_positions.append(pos)
        positions.append(sat_positions)
    return np.array(positions)


def constellation_coverage(constellation: list, ground_points: NDArray, time: object) -> NDArray:
    coverage = []
    for point in ground_points:
        covered = False
        for sat in constellation:
            pos = sat.get_position_eci(time)
            el = math.degrees(math.asin(pos[2] / np.linalg.norm(pos)))
            if el > 5.0:
                covered = True
                break
        coverage.append(covered)
    return np.array(coverage)
