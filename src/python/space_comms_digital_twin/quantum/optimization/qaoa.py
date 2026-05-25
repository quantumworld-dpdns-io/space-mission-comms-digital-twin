from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class QAOResult:
    optimal_parameters: List[float] = field(default_factory=list)
    optimal_value: float = 0.0
    approximation_ratio: float = 0.0
    n_layers: int = 1
    circuit_depth: int = 0
    iterations: int = 0


class QAOA:
    def __init__(self, n_layers: int = 1, optimizer: str = "COBYLA"):
        self.p = n_layers
        self.optimizer = optimizer

    def build_maxcut_hamiltonian(self, edges: List[Tuple[int, int]], n_qubits: int) -> np.ndarray:
        dim = 2 ** n_qubits
        H = np.zeros((dim, dim))
        for i, j in edges:
            for k in range(dim):
                bits = [(k >> q) & 1 for q in range(n_qubits)]
                if bits[i] != bits[j]:
                    H[k, k] += 1.0
        return H

    def build_ising_hamiltonian(self, J: np.ndarray, h: np.ndarray) -> np.ndarray:
        n = len(h)
        dim = 2 ** n
        H = np.zeros((dim, dim))
        for k in range(dim):
            bits = [((k >> q) & 1) * 2 - 1 for q in range(n)]
            for i in range(n):
                H[k, k] += h[i] * bits[i]
                for j in range(i + 1, n):
                    H[k, k] += J[i, j] * bits[i] * bits[j]
        return H

    def solve(self, problem_hamiltonian: np.ndarray,
              initial_params: Optional[List[float]] = None,
              max_iterations: int = 1000) -> QAOResult:
        n_qubits = int(math.log2(len(problem_hamiltonian)))
        if initial_params is None:
            initial_params = [np.random.uniform(0, 2 * math.pi) for _ in range(2 * self.p)]

        params = list(initial_params)
        history = []

        for iteration in range(max_iterations):
            gamma = params[:self.p]
            beta = params[self.p:]

            state = np.zeros(len(problem_hamiltonian), dtype=complex)
            state[0] = 1.0

            for layer in range(self.p):
                phase = np.exp(-1j * gamma[layer] * problem_hamiltonian)
                state = phase @ state

                for q in range(n_qubits):
                    rot = np.array([
                        [math.cos(beta[layer]), -math.sin(beta[layer])],
                        [math.sin(beta[layer]), math.cos(beta[layer])],
                    ])
                    state = self._apply_1q_gate(state, n_qubits, q, rot)

            energy = np.real(np.dot(state.conj(), problem_hamiltonian @ state))
            history.append(energy)

            if self.optimizer == "COBYLA" and len(history) >= 2:
                delta = history[-1] - history[-2]
                if abs(delta) < 1e-6:
                    break

            for i in range(len(params)):
                eps = 0.01
                params_p = list(params)
                params_p[i] += eps
                params_m = list(params)
                params_m[i] -= eps

                gamma_p = params_p[:self.p]
                beta_p = params_p[self.p:]
                gamma_m = params_m[:self.p]
                beta_m = params_m[self.p:]

                state_p = np.zeros(len(problem_hamiltonian), dtype=complex)
                state_p[0] = 1.0
                state_m = np.zeros(len(problem_hamiltonian), dtype=complex)
                state_m[0] = 1.0

                for layer in range(self.p):
                    state_p = np.exp(-1j * gamma_p[layer] * problem_hamiltonian) @ state_p
                    state_m = np.exp(-1j * gamma_m[layer] * problem_hamiltonian) @ state_m

                energy_p = np.real(np.dot(state_p.conj(), problem_hamiltonian @ state_p))
                energy_m = np.real(np.dot(state_m.conj(), problem_hamiltonian @ state_m))
                grad = (energy_p - energy_m) / (2.0 * eps)
                params[i] -= 0.01 * grad

        final_state = np.zeros(len(problem_hamiltonian), dtype=complex)
        final_state[0] = 1.0
        for layer in range(self.p):
            final_state = np.exp(-1j * params[layer] * problem_hamiltonian) @ final_state
        final_energy = np.real(np.dot(final_state.conj(), problem_hamiltonian @ final_state))

        gs_energy = np.min(np.linalg.eigvalsh(problem_hamiltonian))
        approx_ratio = final_energy / gs_energy if gs_energy < 0 else 0.0

        return QAOResult(
            optimal_parameters=params,
            optimal_value=float(final_energy),
            approximation_ratio=float(min(approx_ratio, 1.0)),
            n_layers=self.p,
            circuit_depth=self.p * (len(problem_hamiltonian) + 1),
            iterations=iteration + 1,
        )

    @staticmethod
    def _apply_1q_gate(state: np.ndarray, n_qubits: int, qubit: int,
                        gate: np.ndarray) -> np.ndarray:
        dim = len(state)
        new_state = np.zeros(dim, dtype=complex)
        for k in range(dim):
            bit = (k >> qubit) & 1
            pair = k ^ (bit << qubit)
            if bit == 0:
                new_state[k] = gate[0, 0] * state[k] + gate[0, 1] * state[pair]
            else:
                new_state[k] = gate[1, 0] * state[pair] + gate[1, 1] * state[k]
        return new_state
