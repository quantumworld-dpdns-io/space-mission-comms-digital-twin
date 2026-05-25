import pytest
from space_comms_digital_twin.quantum.simulation.backend_interface import BackendResult


def test_backend_result_defaults():
    result = BackendResult(backend_name="test", shots=1024)
    assert result.backend_name == "test"
    assert result.shots == 1024
    assert result.counts == {}


def test_qiskit_backend_circuit():
    pytest.importorskip("qiskit")
    from qiskit import QuantumCircuit
    from space_comms_digital_twin.quantum.simulation.qiskit_backend import QiskitBackend

    backend = QiskitBackend()
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    result = backend.run_circuit(qc, shots=100)
    assert sum(result.counts.values()) == 100


def test_cirq_backend_creation():
    from space_comms_digital_twin.quantum.simulation.cirq_backend import CirqBackend
    backend = CirqBackend()
    assert backend.name() == "cirq"
    assert backend.max_qubits() == 25


def test_hybrid_simulator_registration():
    from space_comms_digital_twin.quantum.simulation.hybrid_simulator import HybridSimulator
    sim = HybridSimulator()
    assert sim.available_count >= 0


def test_qutip_backend():
    pytest.importorskip("qutip")
    from space_comms_digital_twin.quantum.simulation.qutip_backend import QuTiPBackend
    backend = QuTiPBackend()
    circuit = {
        "qubits": 2,
        "operations": [
            {"gate": "H", "qubits": [0]},
            {"gate": "CNOT", "qubits": [0, 1]},
        ],
    }
    result = backend.run_circuit(circuit)
    assert result.probabilities
