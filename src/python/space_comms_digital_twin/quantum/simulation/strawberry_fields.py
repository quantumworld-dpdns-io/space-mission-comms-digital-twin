from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np

from space_comms_digital_twin.quantum.simulation.backend_interface import (
    BackendResult,
    QuantumBackend,
)


class StrawberryFieldsBackend(QuantumBackend):
    def name(self) -> str:
        return "strawberryfields"

    def supports_simulation(self) -> bool:
        return True

    def max_qubits(self) -> int:
        return 6

    def gate_set(self) -> List[str]:
        return ["Sgate", "Dgate", "BSgate", "S2gate", "Rgate", "Kgate",
                "MeasureFock", "MeasureHomodyne", "MeasureHeterodyne"]

    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult:
        try:
            import strawberryfields as sf
            from strawberryfields import ops

            n_modes = circuit.get("qubits", 2)
            prog = sf.Program(n_modes)

            with prog.context as q:
                for op_def in circuit.get("operations", []):
                    gate = op_def.get("gate", "")
                    targets = op_def.get("qubits", [0])
                    params = op_def.get("params", [])
                    if gate == "Sgate" and params:
                        ops.Sgate(*params) | q[targets[0]]
                    elif gate == "Dgate" and params:
                        ops.Dgate(*params) | q[targets[0]]
                    elif gate == "BSgate":
                        ops.BSgate() | (q[targets[0]], q[targets[1]])
                    elif gate == "Rgate" and params:
                        ops.Rgate(params[0]) | q[targets[0]]
                    elif gate == "MeasureFock":
                        ops.MeasureFock() | q[targets[0]]

            eng = sf.Engine("fock", cutoff_dim=kwargs.get("cutoff_dim", 6))
            result = eng.run(prog)
            samples = result.samples

            return BackendResult(
                counts={"0": len(samples)},
                shots=shots,
                backend_name=self.name(),
                metadata={"simulator": "strawberryfields-fock", "cutoff_dim": 6},
            )
        except ImportError:
            raise ImportError("Strawberry Fields not installed. Install with: pip install strawberryfields")

    def get_noise_model(self) -> Optional[Any]:
        return {"loss": 0.1, "phase_noise": 0.01}

    def estimate_resources(self, circuit: Any) -> Dict[str, Any]:
        return {"modes": circuit.get("qubits", 0), "gates": len(circuit.get("operations", [])), "cutoff_dim": 6}
