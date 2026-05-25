from __future__ import annotations

from typing import Any

import numpy as np

from space_comms_digital_twin.quantum.simulation.backend_interface import (
    BackendResult,
    QuantumBackend,
)


class CirqBackend(QuantumBackend):
    def name(self) -> str:
        return "cirq"

    def supports_simulation(self) -> bool:
        return True

    def max_qubits(self) -> int:
        return 25

    def gate_set(self) -> list[str]:
        return ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "SWAP",
                "ISWAP", "CCX", "CCZ", "RX", "RY", "RZ", "XPow", "ZPow", "PhasedXPow"]

    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult:
        try:
            import cirq
            simulator = cirq.Simulator()
            if shots > 0:
                result = simulator.run(circuit, repetitions=shots)
                counts = result.histogram(key="m" if "m" in result.measurements else next(iter(result.measurements.keys())))
                str_counts = {format(k, f'0{circuit.all_qubits().__len__() if circuit.all_qubits() else 1}b'): v for k, v in counts.items()}
                return BackendResult(
                    counts=str_counts,
                    shots=shots,
                    backend_name=self.name(),
                )
            result = simulator.simulate(circuit)
            state = result.final_state_vector
            probs = np.abs(state) ** 2
            str_probs = {format(i, f'0{int(np.log2(len(probs)))}b'): float(p) for i, p in enumerate(probs)}
            return BackendResult(
                probabilities=str_probs,
                state_vector=state,
                shots=0,
                backend_name=self.name(),
            )
        except ImportError:
            raise ImportError("Cirq not installed. Install with: pip install cirq")

    def get_noise_model(self) -> Any | None:
        try:
            import cirq
            return cirq.ConstantQubitNoiseModel(cirq.depolarize(0.01))
        except ImportError:
            return None

    def estimate_resources(self, circuit: Any) -> dict[str, Any]:
        try:
            moments = len(circuit)
            ops = sum(1 for _ in circuit.all_operations())
            qubits = len(circuit.all_qubits())
            return {"qubits": qubits, "gates": ops, "depth": moments}
        except Exception:
            return {"qubits": 0, "gates": 0, "depth": 0}
