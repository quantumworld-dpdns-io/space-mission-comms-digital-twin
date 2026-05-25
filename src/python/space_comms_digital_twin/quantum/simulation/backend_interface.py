from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BackendResult:
    counts: Dict[str, int] = field(default_factory=dict)
    probabilities: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    state_vector: Optional[Any] = None
    expectation_values: Optional[Dict[str, float]] = None
    shots: int = 0
    backend_name: str = ""
    execution_time_ms: float = 0.0
    fidelity: Optional[float] = None


class QuantumBackend(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def supports_simulation(self) -> bool: ...

    @abstractmethod
    def max_qubits(self) -> int: ...

    @abstractmethod
    def gate_set(self) -> List[str]: ...

    @abstractmethod
    def run_circuit(self, circuit: Any, shots: int = 1024, **kwargs: Any) -> BackendResult: ...

    def get_noise_model(self) -> Optional[Any]:
        return None

    def validate_circuit(self, circuit: Any) -> bool:
        return True

    def estimate_resources(self, circuit: Any) -> Dict[str, Any]:
        return {"qubits": 0, "gates": 0, "depth": 0}

    def calibrate(self) -> Dict[str, Any]:
        return {"status": "ok"}
