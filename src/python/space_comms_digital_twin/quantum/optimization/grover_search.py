from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional

import numpy as np


@dataclass
class GroverResult:
    found_solution: Optional[int] = None
    n_iterations: int = 0
    success_probability: float = 0.0
    optimal_iterations: int = 0
    n_qubits: int = 0


class GroverSearch:
    def __init__(self, n_qubits: int = 3):
        self.n_qubits = n_qubits
        self.dim = 2 ** n_qubits

    def oracle(self, marked_state: int) -> np.ndarray:
        O = np.eye(self.dim)
        O[marked_state, marked_state] = -1
        return O

    def phase_oracle(self, predicate: Callable[[int], bool]) -> np.ndarray:
        O = np.eye(self.dim)
        for i in range(self.dim):
            if predicate(i):
                O[i, i] = -1
        return O

    def diffusion(self) -> np.ndarray:
        D = np.ones((self.dim, self.dim)) * (2.0 / self.dim)
        D -= np.eye(self.dim)
        return D

    def search(self, oracle_matrix: np.ndarray, num_solutions: int = 1) -> GroverResult:
        optimal_iters = int((math.pi / 4) * math.sqrt(self.dim / num_solutions))
        n_iters = max(1, optimal_iters)

        state = np.ones(self.dim, dtype=complex) / math.sqrt(self.dim)

        D = self.diffusion()
        for _ in range(n_iters):
            state = oracle_matrix @ state
            state = D @ state

        probs = np.abs(state) ** 2
        found = int(np.argmax(probs))

        return GroverResult(
            found_solution=found,
            n_iterations=n_iters,
            success_probability=float(probs[found]),
            optimal_iterations=optimal_iters,
            n_qubits=self.n_qubits,
        )

    def amplitude_amplification(self, oracle_matrix: np.ndarray,
                                 n_iterations: int = 1) -> np.ndarray:
        state = np.ones(self.dim, dtype=complex) / math.sqrt(self.dim)
        D = self.diffusion()
        for _ in range(n_iterations):
            state = oracle_matrix @ state
            state = D @ state
        return state

    def optimal_iteration_count(self, num_solutions: int = 1) -> int:
        return max(1, int((math.pi / 4) * math.sqrt(self.dim / num_solutions)))

    def fixed_point_search(self, oracle_matrix: np.ndarray) -> GroverResult:
        lambda_val = 1.0
        for k in range(1, 100):
            theta_k = math.pi / (2.0 * k + 2.0)
            state = np.ones(self.dim, dtype=complex) / math.sqrt(self.dim)
            for _ in range(k):
                state = oracle_matrix @ state
                D = self.diffusion()
                state = D @ state

            probs = np.abs(state) ** 2
            found = int(np.argmax(probs))
            if probs[found] > 0.9:
                return GroverResult(
                    found_solution=found,
                    n_iterations=k,
                    success_probability=float(probs[found]),
                    optimal_iterations=k,
                    n_qubits=self.n_qubits,
                )

        return self.search(oracle_matrix)
