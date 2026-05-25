from __future__ import annotations

from typing import Any, Dict, List, Optional

from space_comms_digital_twin.quantum.simulation.backend_interface import (
    BackendResult,
    QuantumBackend,
)


class QiskitBackend(QuantumBackend):
    def name(self) -> str:
        return "qiskit"

    def supports_simulation(self) -> bool:
        return True

    def max_qubits(self) -> int:
        return 32

    def gate_set(self) -> List[str]:
        return ["H", "X", "Y", "Z", "S", "T", "SDG", "TDG", "SX", "CNOT", "CZ",
                "SWAP", "CCX", "RX", "RY", "RZ", "CRX", "CRY", "CRZ", "U1", "U2", "U3"]

    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult:
        try:
            from qiskit_aer import AerSimulator
            simulator = AerSimulator()
            compiled = simulator.run(circuit, shots=shots)
            result = compiled.result()
            counts = result.get_counts()
            return BackendResult(
                counts=counts,
                shots=shots,
                backend_name=self.name(),
                metadata={"simulator": "qiskit-aer", "noise": kwargs.get("noise", False)},
            )
        except ImportError:
            raise ImportError("Qiskit not installed. Install with: pip install qiskit qiskit-aer")

    def get_noise_model(self) -> Optional[Any]:
        try:
            from qiskit_aer.noise import NoiseModel
            return NoiseModel()
        except ImportError:
            return None

    def validate_circuit(self, circuit: Any) -> bool:
        try:
            circuit.count_ops()
            return True
        except Exception:
            return False

    def estimate_resources(self, circuit: Any) -> Dict[str, Any]:
        try:
            ops = circuit.count_ops()
            depth = circuit.depth()
            qubits = circuit.num_qubits
            return {"qubits": qubits, "gates": sum(ops.values()), "depth": depth, "operations": ops}
        except Exception:
            return {"qubits": 0, "gates": 0, "depth": 0}

    def calibrate(self) -> Dict[str, Any]:
        return {"status": "ok", "simulator": "qiskit-aer", "version": "1.0+"}
