from fastapi.testclient import TestClient
from space_comms_digital_twin.api.rest.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "docs" in response.json()


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200


def test_simulation_run():
    params = {"tx_power": 10.0, "frequency": 8.0, "distance": 1e6}
    response = client.post("/api/v1/simulation/run", json=params)
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data


def test_simulation_status():
    params = {"tx_power": 10.0, "frequency": 8.0, "distance": 1e6}
    create = client.post("/api/v1/simulation/run", json=params)
    job_id = create.json()["job_id"]
    response = client.get(f"/api/v1/simulation/status/{job_id}")
    assert response.status_code == 200


def test_simulation_history():
    response = client.get("/api/v1/simulation/history")
    assert response.status_code == 200


def test_quantum_backends():
    response = client.get("/api/v1/quantum/backends")
    assert response.status_code == 200
    assert "backends" in response.json()


def test_optimization_jobs():
    response = client.get("/api/v1/optimization/jobs")
    assert response.status_code == 200


def test_route_optimization():
    graph = {
        "A": {"B": 1.0, "C": 4.0},
        "B": {"C": 2.0, "D": 5.0},
        "C": {"D": 1.0},
        "D": {},
    }
    response = client.post(
        "/api/v1/optimization/route",
        json={"graph": graph, "source": "A", "target": "D"},
    )
    assert response.status_code == 200
