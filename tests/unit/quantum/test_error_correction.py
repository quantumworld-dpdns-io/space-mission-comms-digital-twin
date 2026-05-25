import pytest
from space_comms_digital_twin.quantum.comms.error_correction import (
    RepetitionCode,
    ShorCode,
    SteaneCode,
    SurfaceCode,
    get_error_correction_code,
)


def test_repetition_code_logical_error_rate():
    code = RepetitionCode(distance=3)
    rate = code.logical_error_rate(0.1)
    assert 0 < rate < 1
    assert code.name() == "RepetitionCode(d=3)"


def test_shor_code():
    code = ShorCode()
    rate = code.logical_error_rate(0.1)
    assert rate > 0


def test_steane_code():
    code = SteaneCode()
    rate = code.logical_error_rate(0.01)
    assert rate < 0.01


def test_surface_code():
    code = SurfaceCode(distance=3)
    rate = code.logical_error_rate(0.001)
    assert rate > 0


def test_get_code_by_name():
    code = get_error_correction_code("repetition_3")
    assert isinstance(code, RepetitionCode)
    code = get_error_correction_code("shor_9")
    assert isinstance(code, ShorCode)


def test_code_thresholds():
    assert RepetitionCode().threshold() == 0.5
    assert ShorCode().threshold() > 0
