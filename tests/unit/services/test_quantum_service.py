import pytest
from space_comms_digital_twin.services.quantum_service import QuantumService


def test_list_backends():
    service = QuantumService()
    backends = service.list_backends()
    assert isinstance(backends, list)


def test_run_qkd():
    service = QuantumService()
    job = service.run_qkd(protocol="BB84", num_bits=128)
    assert job.status == "completed"
    assert job.result is not None


def test_run_teleport():
    service = QuantumService()
    job = service.run_teleportation()
    assert job.status == "completed"


def test_get_job():
    service = QuantumService()
    job = service.run_qkd()
    retrieved = service.get_job(job.id)
    assert retrieved is not None
