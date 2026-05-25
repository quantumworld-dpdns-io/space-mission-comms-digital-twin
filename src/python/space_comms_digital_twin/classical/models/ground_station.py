from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from space_comms_digital_twin.config import EARTH_RADIUS


@dataclass
class GroundStation:
    id: str
    name: str
    latitude: float
    longitude: float
    altitude: float = 0.0
    elevation_mask: float = 5.0
    site_type: str = "fixed"
    antennas: list[str] = field(default_factory=list)
    operator: str = ""
    timezone: str = "UTC"

    def __post_init__(self) -> None:
        self._lat_rad = math.radians(self.latitude)
        self._lon_rad = math.radians(self.longitude)

    def to_geocentric(self) -> np.ndarray:
        r = EARTH_RADIUS + self.altitude
        x = r * math.cos(self._lat_rad) * math.cos(self._lon_rad)
        y = r * math.cos(self._lat_rad) * math.sin(self._lon_rad)
        z = r * math.sin(self._lat_rad)
        return np.array([x, y, z])

    def get_ecef_coords(self) -> np.ndarray:
        return self.to_geocentric()

    def get_horizon_coords(self, sat_eci: np.ndarray, sat_epoch: object = None) -> tuple[float, float, float]:
        station_ecef = self.to_geocentric()

        gmst = self._compute_gmst()

        rotation = np.array([
            [math.cos(gmst), math.sin(gmst), 0.0],
            [-math.sin(gmst), math.cos(gmst), 0.0],
            [0.0, 0.0, 1.0],
        ])
        sat_ecef = rotation @ sat_eci
        los = sat_ecef - station_ecef

        rlos = np.linalg.norm(los)
        if rlos < 1e-6:
            return (0.0, 0.0, 0.0)

        sin_lat = math.sin(self._lat_rad)
        cos_lat = math.cos(self._lat_rad)
        sin_lon = math.sin(self._lon_rad)
        cos_lon = math.cos(self._lon_rad)

        top = np.array([
            [-sin_lon, cos_lon, 0.0],
            [-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat],
            [cos_lat * cos_lon, cos_lat * sin_lon, sin_lat],
        ]) @ los

        az = math.degrees(math.atan2(top[0], top[1]))
        if az < 0:
            az += 360.0

        el = math.degrees(math.asin(top[2] / rlos))
        return (az, el, rlos)

    def is_satellite_visible(self, sat_eci: np.ndarray, epoch: object = None) -> bool:
        _, el, _ = self.get_horizon_coords(sat_eci, epoch)
        return el >= self.elevation_mask

    def get_az_el_range(self, sat_eci: np.ndarray, epoch: object = None) -> tuple[float, float, float]:
        return self.get_horizon_coords(sat_eci, epoch)

    @staticmethod
    def _compute_gmst() -> float:
        from astropy.time import Time
        t = Time.now()
        return t.sidereal_time('mean', 'greenwich').rad

    def time_to_aos(self, sat_eci_func: object) -> float | None:
        return None

    def time_to_los(self, sat_eci_func: object) -> float | None:
        return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "elevation_mask": self.elevation_mask,
            "site_type": self.site_type,
            "antennas": self.antennas,
            "operator": self.operator,
        }

    def __repr__(self) -> str:
        return f"GroundStation(id='{self.id}', name='{self.name}', lat={self.latitude}, lon={self.longitude})"
