from space_comms_digital_twin.services.simulation_service import SimulationService


def test_run_and_get():
    service = SimulationService()
    job = service.run_classical_simulation({"tx_power": 10.0})
    assert job.status == "completed"
    status = service.get_simulation_status(job.id)
    assert status is not None


def test_cancel():
    service = SimulationService()
    result = service.cancel_simulation("nonexistent")
    assert result is False


def test_list():
    service = SimulationService()
    service.run_classical_simulation({"tx_power": 5.0})
    sims = service.list_simulations()
    assert len(sims) >= 1
