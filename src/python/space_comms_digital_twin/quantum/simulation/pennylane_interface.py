from __future__ import annotations

from collections.abc import Callable
from typing import Any

from space_comms_digital_twin.quantum.simulation.backend_interface import (
    BackendResult,
    QuantumBackend,
)


class PennyLaneInterface(QuantumBackend):
    def name(self) -> str:
        return "pennylane"

    def supports_simulation(self) -> bool:
        return True

    def max_qubits(self) -> int:
        return 20

    def gate_set(self) -> list[str]:
        return ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "SWAP",
                "RX", "RY", "RZ", "CRX", "CRY", "CRZ", "QubitUnitary"]

    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult:
        try:
            import pennylane as qml
            n_qubits = circuit.get("qubits", 2)
            ops = circuit.get("operations", [])
            dev = qml.device("default.qubit", wires=n_qubits, shots=shots)

            @qml.qnode(dev)
            def _circuit():
                for op in ops:
                    gate = op.get("gate", "")
                    targets = op.get("qubits", [0])
                    params = op.get("params", [])
                    if gate == "H":
                        qml.Hadamard(wires=targets[0])
                    elif gate == "X":
                        qml.PauliX(wires=targets[0])
                    elif gate == "Y":
                        qml.PauliY(wires=targets[0])
                    elif gate == "Z":
                        qml.PauliZ(wires=targets[0])
                    elif gate == "CNOT":
                        qml.CNOT(wires=targets)
                    elif gate == "CZ":
                        qml.CZ(wires=targets)
                    elif gate == "RX" and params:
                        qml.RX(params[0], wires=targets[0])
                    elif gate == "RY" and params:
                        qml.RY(params[0], wires=targets[0])
                    elif gate == "RZ" and params:
                        qml.RZ(params[0], wires=targets[0])
                return qml.counts()

            counts = _circuit()
            return BackendResult(
                counts=dict(counts),
                shots=shots,
                backend_name=self.name(),
                metadata={"framework": "pennylane", "device": "default.qubit"},
            )
        except ImportError:
            raise ImportError("PennyLane not installed. Install with: pip install pennylane")

    def get_vqe_circuit(self, n_qubits: int, layers: int = 2) -> Callable:
        try:
            import pennylane as qml

            def circuit(params):
                for i in range(n_qubits):
                    qml.RY(params[i], wires=i)
                for layer in range(layers):
                    for i in range(n_qubits - 1):
                        qml.CNOT(wires=[i, i + 1])
                    offset = layers * n_qubits + layer * n_qubits
                    for i in range(n_qubits):
                        qml.RZ(params[offset + i], wires=i)
                return qml.expval(qml.PauliZ(0))

            return circuit
        except ImportError:
            raise ImportError("PennyLane not installed")

    def estimate_resources(self, circuit: Any) -> dict[str, Any]:
        return {"qubits": circuit.get("qubits", 0), "gates": len(circuit.get("operations", [])), "depth": 0}
