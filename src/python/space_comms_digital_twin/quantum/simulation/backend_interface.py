from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BackendResult:
    counts: dict[str, int] = field(default_factory=dict)
    probabilities: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    state_vector: Any | None = None
    expectation_values: dict[str, float] | None = None
    shots: int = 0
    backend_name: str = ""
    execution_time_ms: float = 0.0
    fidelity: float | None = None


class QuantumBackend(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def supports_simulation(self) -> bool: ...

    @abstractmethod
    def max_qubits(self) -> int: ...

    @abstractmethod
    def gate_set(self) -> list[str]: ...

    @abstractmethod
    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult: ...

    def get_noise_model(self) -> Any | None:
        return None

    def validate_circuit(self, circuit: Any) -> bool:
        return True

    def estimate_resources(self, circuit: Any) -> dict[str, Any]:
        return {"qubits": 0, "gates": 0, "depth": 0}

    def calibrate(self) -> dict[str, Any]:
        return {"status": "ok"}
