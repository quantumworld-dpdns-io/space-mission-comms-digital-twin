import pytest


@pytest.fixture
def sample_tle() -> str:
    return (
        "1 25544U 98067A   24001.50000000  .00001234  00000+0  12345-4 0  9991\n"
        "2 25544  51.6420 123.4567 0001234 123.4567 234.5678 15.50123456123456"
    )


@pytest.fixture
def sample_orbit_elements() -> dict:
    return {
        "inclination": 51.6,
        "raan": 123.4,
        "eccentricity": 0.0001234,
        "arg_perigee": 123.5,
        "mean_anomaly": 234.6,
        "mean_motion": 15.5,
    }


@pytest.fixture
def sample_quantum_circuit() -> dict:
    return {
        "qubits": 2,
        "operations": [
            {"gate": "H", "qubits": [0]},
            {"gate": "CNOT", "qubits": [0, 1]},
            {"gate": "MEASURE", "qubits": [0], "classical": [0]},
            {"gate": "MEASURE", "qubits": [1], "classical": [1]},
        ],
    }


@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setenv("APP_NAME", "test-app")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("API_HOST", "127.0.0.1")
    monkeypatch.setenv("API_PORT", "8000")
    monkeypatch.setenv("AUTH_SECRET_KEY", "test-key-not-for-prod")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("QUANTUM_BACKENDS", '["qiskit","cirq"]')
    from space_comms_digital_twin.config import settings
    return settings
