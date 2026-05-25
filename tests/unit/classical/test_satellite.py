import pytest
from space_comms_digital_twin.classical.models.satellite import Satellite


def test_satellite_from_tle(sample_tle):
    lines = sample_tle.strip().split("\n")
    sat = Satellite.from_tle(25544, lines[0], lines[1], name="ISS")
    assert sat.norad_id == 25544
    assert sat.name == "ISS"
    assert sat.inclination > 0


def test_satellite_propagate(sample_tle):
    from datetime import datetime, timezone
    lines = sample_tle.strip().split("\n")
    sat = Satellite.from_tle(25544, lines[0], lines[1])
    pos, vel = sat.propagate_to(datetime.now(timezone.utc))
    assert len(pos) == 3
    assert len(vel) == 3


def test_satellite_invalid_id():
    with pytest.raises((ValueError, TypeError)):
        Satellite(norad_id=-1)


def test_satellite_to_dict(sample_tle):
    lines = sample_tle.strip().split("\n")
    sat = Satellite.from_tle(25544, lines[0], lines[1])
    d = sat.to_dict()
    assert d["norad_id"] == 25544
    assert "inclination" in d
    assert "apogee_altitude" in d
