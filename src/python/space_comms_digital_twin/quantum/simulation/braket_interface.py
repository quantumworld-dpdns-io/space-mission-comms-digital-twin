from __future__ import annotations

from typing import Any, Dict, List, Optional

from space_comms_digital_twin.quantum.simulation.backend_interface import (
    BackendResult,
    QuantumBackend,
)


class BraketBackend(QuantumBackend):
    def name(self) -> str:
        return "amazon-braket"

    def supports_simulation(self) -> bool:
        return True

    def max_qubits(self) -> int:
        return 25

    def gate_set(self) -> List[str]:
        return ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "SWAP",
                "RX", "RY", "RZ", "PHASE", "XX", "YY", "ZZ", "CCNOT"]

    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult:
        try:
            from braket.devices import LocalSimulator
            from braket.circuits import Circuit as BraketCircuit

            device = LocalSimulator()
            bc = BraketCircuit()

            ops = circuit.get("operations", [])
            for op in ops:
                gate = op.get("gate", "")
                targets = op.get("qubits", [0])
                params = op.get("params", [])
                if gate == "H":
                    bc.h(targets[0])
                elif gate == "X":
                    bc.x(targets[0])
                elif gate == "Y":
                    bc.y(targets[0])
                elif gate == "Z":
                    bc.z(targets[0])
                elif gate == "CNOT":
                    bc.cnot(targets[0], targets[1])
                elif gate == "CZ":
                    bc.cz(targets[0], targets[1])
                elif gate == "SWAP":
                    bc.swap(targets[0], targets[1])
                elif gate == "RX" and params:
                    bc.rx(targets[0], params[0])
                elif gate == "RY" and params:
                    bc.ry(targets[0], params[0])
                elif gate == "RZ" and params:
                    bc.rz(targets[0], params[0])

            result = device.run(bc, shots=shots).result()
            counts = result.measurement_counts
            str_counts = {k: v for k, v in counts.items()}

            return BackendResult(
                counts=str_counts,
                shots=shots,
                backend_name=self.name(),
                metadata={"simulator": "braket-local"},
            )
        except ImportError:
            raise ImportError("Amazon Braket SDK not installed. Install with: pip install amazon-braket-sdk")

    def estimate_resources(self, circuit: Any) -> Dict[str, Any]:
        return {"qubits": circuit.get("qubits", 0), "gates": len(circuit.get("operations", [])), "depth": 0}
