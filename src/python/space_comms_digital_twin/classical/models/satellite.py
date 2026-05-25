from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

import numpy as np
from sgp4.api import Satrec, jday


@dataclass
class Satellite:
    norad_id: int
    name: str = ""
    tle_line1: str = ""
    tle_line2: str = ""
    epoch: Optional[datetime] = None
    inclination: float = 0.0
    raan: float = 0.0
    eccentricity: float = 0.0
    arg_perigee: float = 0.0
    mean_anomaly: float = 0.0
    mean_motion: float = 0.0
    bstar: float = 0.0
    launch_date: Optional[datetime] = None
    satellite_type: str = "LEO"
    owner: str = ""
    _sgp4_sat: Optional[Satrec] = None

    def __post_init__(self) -> None:
        if self.tle_line1 and self.tle_line2:
            self._init_from_tle()

    def _init_from_tle(self) -> None:
        self._sgp4_sat = Satrec.twoline2rv(self.tle_line1, self.tle_line2)
        self.inclination = math.degrees(self._sgp4_sat.inclo)
        self.raan = math.degrees(self._sgp4_sat.nodeo)
        self.eccentricity = self._sgp4_sat.ecco
        self.arg_perigee = math.degrees(self._sgp4_sat.argpo)
        self.mean_anomaly = math.degrees(self._sgp4_sat.mo)
        self.mean_motion = self._sgp4_sat.no * 60.0 / (2.0 * math.pi)

    @classmethod
    def from_tle(cls, norad_id: int, line1: str, line2: str, name: str = "") -> Satellite:
        return cls(norad_id= norad_id, name=name, tle_line1=line1, tle_line2=line2)

    def propagate_to(self, epoch: datetime) -> tuple[np.ndarray, np.ndarray]:
        jd, fr = jday(
            epoch.year, epoch.month, epoch.day,
            epoch.hour, epoch.minute,
            epoch.second + epoch.microsecond / 1e6,
        )
        if self._sgp4_sat is None:
            raise ValueError("No TLE data loaded")
        error_code, pos_eci, vel_eci = self._sgp4_sat.sgp4(jd, fr)
        if error_code != 0:
            raise RuntimeError(f"SGP4 propagation error: {error_code}")
        return np.array(pos_eci) * 1000.0, np.array(vel_eci) * 1000.0

    def get_position_eci(self, epoch: Optional[datetime] = None) -> np.ndarray:
        if epoch is None:
            epoch = datetime.now(timezone.utc)
        pos, _ = self.propagate_to(epoch)
        return pos

    def get_velocity_eci(self, epoch: Optional[datetime] = None) -> np.ndarray:
        if epoch is None:
            epoch = datetime.now(timezone.utc)
        _, vel = self.propagate_to(epoch)
        return vel

    def get_orbit_period(self) -> float:
        return 2.0 * math.pi / (self.mean_motion * 60.0)

    def get_semimajor_axis(self) -> float:
        from space_comms_digital_twin.config import EARTH_MU
        n = self.mean_motion * 2.0 * math.pi / 86400.0
        return (EARTH_MU / (n ** 2)) ** (1.0 / 3.0)

    def is_in_eclipse(self, epoch: Optional[datetime] = None) -> bool:
        if epoch is None:
            epoch = datetime.now(timezone.utc)
        pos = self.get_position_eci(epoch)
        sun_vec = self._sun_vector(epoch)
        norm_pos = np.linalg.norm(pos)
        norm_sun = np.linalg.norm(sun_vec)
        if np.dot(pos, sun_vec) / (norm_pos * norm_sun) > 0:
            return False
        earth_radius = 6371000.0
        shadow_angle = math.asin(earth_radius / norm_pos)
        sun_angle = math.acos(np.dot(pos, sun_vec) / (norm_pos * norm_sun))
        return sun_angle < shadow_angle

    @staticmethod
    def _sun_vector(epoch: datetime) -> np.ndarray:
        from astropy.time import Time
        from astropy.coordinates import get_sun, GCRS
        from astropy.coordinates import SkyCoord
        t = Time(epoch)
        sun = get_sun(t)
        cart = sun.represent_as('cartesian')
        return np.array([cart.x.value, cart.y.value, cart.z.value])

    @property
    def apogee_altitude(self) -> float:
        a = self.get_semimajor_axis()
        return a * (1.0 + self.eccentricity) - 6371000.0

    @property
    def perigee_altitude(self) -> float:
        a = self.get_semimajor_axis()
        return a * (1.0 - self.eccentricity) - 6371000.0

    @property
    def is_leo(self) -> bool:
        return self.apogee_altitude < 2000000.0

    @property
    def is_meo(self) -> bool:
        alt = self.apogee_altitude
        return 2000000.0 <= alt < 35786000.0

    @property
    def is_geo(self) -> bool:
        return abs(self.apogee_altitude - 35786000.0) < 1000000.0

    def to_dict(self) -> dict:
        return {
            "norad_id": self.norad_id,
            "name": self.name,
            "inclination": self.inclination,
            "raan": self.raan,
            "eccentricity": self.eccentricity,
            "arg_perigee": self.arg_perigee,
            "mean_anomaly": self.mean_anomaly,
            "mean_motion": self.mean_motion,
            "apogee_altitude": self.apogee_altitude,
            "perigee_altitude": self.perigee_altitude,
            "orbit_period": self.get_orbit_period(),
            "satellite_type": self.satellite_type,
        }

    def __repr__(self) -> str:
        return f"Satellite(norad_id={self.norad_id}, name='{self.name}', type={self.satellite_type})"
