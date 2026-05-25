from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import numpy as np

from space_comms_digital_twin.quantum.optimization.vqe import VQE, VQEResult


@dataclass
class BandwidthProblem:
    n_users: int = 0
    demands: List[float] = field(default_factory=list)
    total_capacity: float = 0.0
    weights: List[float] = field(default_factory=list)


class BandwidthAllocationVQE:
    def __init__(self, n_layers: int = 2):
        self.n_layers = n_layers
        self.vqe = VQE(n_qubits=4, n_layers=n_layers)

    def build_problem(self, demands: Dict[str, float],
                      total_capacity: float,
                      weights: Dict[str, float]) -> BandwidthProblem:
        n = len(demands)
        return BandwidthProblem(
            n_users=n,
            demands=list(demands.values()),
            total_capacity=total_capacity,
            weights=list(weights.values()) if weights else [1.0] * n,
        )

    def solve(self, problem: BandwidthProblem) -> VQEResult:
        n_qubits = min(4, problem.n_users)
        self.vqe = VQE(n_qubits=n_qubits, n_layers=self.n_layers)

        pauli_terms = []
        for i in range(n_qubits):
            term = ['I'] * n_qubits
            term[i] = 'Z'
            coeff = -(problem.demands[i] / problem.total_capacity) if i < len(problem.demands) else 0.0
            pauli_terms.append(("".join(term), coeff))

        H = self.vqe.build_hamiltonian(pauli_terms)
        result = self.vqe.solve(H)

        return result
