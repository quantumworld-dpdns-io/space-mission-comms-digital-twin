from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from space_comms_digital_twin.quantum.simulation.backend_interface import (
    BackendResult,
    QuantumBackend,
)
from space_comms_digital_twin.utils.logger import get_logger

logger = get_logger(__name__)


class HybridSimulator:
    def __init__(self):
        self.backends: Dict[str, QuantumBackend] = {}
        self._register_default_backends()

    def _register_default_backends(self) -> None:
        backends_to_try = [
            ("qiskit", "QiskitBackend"),
            ("cirq", "CirqBackend"),
            ("pennylane", "PennyLaneInterface"),
            ("qutip", "QuTiPBackend"),
        ]
        for name, cls_name in backends_to_try:
            try:
                mod = __import__(
                    f"space_comms_digital_twin.quantum.simulation.{name}_backend"
                    if name != "pennylane" else
                    f"space_comms_digital_twin.quantum.simulation.{name}_interface",
                    fromlist=[cls_name],
                )
                cls = getattr(mod, cls_name)
                self.register_backend(cls())
                logger.info(f"Registered backend: {name}")
            except Exception as e:
                logger.debug(f"Skipping backend {name}: {e}")

    def register_backend(self, backend: QuantumBackend) -> None:
        self.backends[backend.name()] = backend

    def get_backend(self, name: str) -> Optional[QuantumBackend]:
        return self.backends.get(name)

    def list_backends(self) -> List[Dict[str, Any]]:
        return [
            {"name": b.name(), "max_qubits": b.max_qubits(), "gate_set": b.gate_set()}
            for b in self.backends.values()
        ]

    def run_on_all(self, circuit: Any, shots: int = 1024,
                   filter_backends: Optional[List[str]] = None) -> Dict[str, BackendResult]:
        results = {}
        for name, backend in self.backends.items():
            if filter_backends and name not in filter_backends:
                continue
            try:
                t0 = time.monotonic()
                result = backend.run_circuit(circuit, shots=shots)
                result.execution_time_ms = (time.monotonic() - t0) * 1000.0
                results[name] = result
            except Exception as e:
                logger.error(f"Backend {name} failed: {e}")
        return results

    def run_best(self, circuit: Any, shots: int = 1024,
                 criteria: str = "accuracy") -> BackendResult:
        results = self.run_on_all(circuit, shots=shots)
        if not results:
            raise RuntimeError("No backends available")
        best_name = min(results.keys())
        return results[best_name]

    def compare_backends(self, circuit: Any, shots: int = 1024) -> Dict[str, Any]:
        results = self.run_on_all(circuit, shots=shots)
        comparison = {}
        for name, result in results.items():
            comparison[name] = {
                "counts": result.counts,
                "execution_time_ms": result.execution_time_ms,
                "fidelity": result.fidelity,
            }
        return comparison

    def estimate_resources(self, circuit: Any) -> Dict[str, Any]:
        total = {"qubits": 0, "gates": 0}
        for backend in self.backends.values():
            est = backend.estimate_resources(circuit)
            total["qubits"] = max(total["qubits"], est.get("qubits", 0))
            total["gates"] = max(total["gates"], est.get("gates", 0))
        return total

    @property
    def available_count(self) -> int:
        return len(self.backends)
