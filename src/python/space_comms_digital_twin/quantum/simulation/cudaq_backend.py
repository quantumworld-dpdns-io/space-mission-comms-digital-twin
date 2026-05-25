from __future__ import annotations

from typing import Any

from space_comms_digital_twin.quantum.simulation.backend_interface import (
    BackendResult,
    QuantumBackend,
)


class CUDAQBackend(QuantumBackend):
    def name(self) -> str:
        return "cudaq"

    def supports_simulation(self) -> bool:
        return True

    def max_qubits(self) -> int:
        return 30

    def gate_set(self) -> list[str]:
        return ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "SWAP", "RX", "RY", "RZ"]

    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult:
        try:
            import cudaq
            sample_result = cudaq.sample(circuit, shots_count=shots)
            counts = {k: v for k, v in sample_result.items()}
            return BackendResult(
                counts=counts,
                shots=shots,
                backend_name=self.name(),
                metadata={"gpu": True, "platform": "cuda-q"},
            )
        except ImportError:
            raise ImportError("CUDA-Q not installed. Install with: pip install cudaq")

    def get_noise_model(self) -> Any | None:
        try:
            import cudaq
            noise = cudaq.NoiseModel()
            return noise
        except ImportError:
            return None

    def estimate_resources(self, circuit: Any) -> dict[str, Any]:
        return {"qubits": 2, "gates": 2, "depth": 2, "gpu_required": True}
