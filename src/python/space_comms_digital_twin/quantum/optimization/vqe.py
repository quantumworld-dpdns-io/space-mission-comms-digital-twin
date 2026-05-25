from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class VQEResult:
    optimal_parameters: List[float] = field(default_factory=list)
    optimal_energy: float = 0.0
    n_iterations: int = 0
    convergence: List[float] = field(default_factory=list)
    ansatz_depth: int = 0
    n_qubits: int = 0


class VQE:
    def __init__(self, n_qubits: int = 2, n_layers: int = 2, optimizer: str = "SPSA"):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.optimizer = optimizer

    def build_hamiltonian(self, pauli_terms: List[Tuple[str, float]]) -> np.ndarray:
        dim = 2 ** self.n_qubits
        H = np.zeros((dim, dim), dtype=complex)

        sx = np.array([[0, 1], [1, 0]], dtype=complex)
        sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
        sz = np.array([[1, 0], [0, -1]], dtype=complex)
        si = np.eye(2, dtype=complex)

        for term, coeff in pauli_terms:
            op = 1.0
            for p in term:
                if p == 'I':
                    op = np.kron(op, si)
                elif p == 'X':
                    op = np.kron(op, sx)
                elif p == 'Y':
                    op = np.kron(op, sy)
                elif p == 'Z':
                    op = np.kron(op, sz)
            H += coeff * op

        return np.real(H)

    def _hardware_efficient_ansatz(self, params: np.ndarray) -> np.ndarray:
        state = np.zeros(2 ** self.n_qubits, dtype=complex)
        state[0] = 1.0

        for q in range(self.n_qubits):
            state = self._apply_1q_gate(state, self.n_qubits, q,
                                        np.array([[math.cos(params[q]), -math.sin(params[q])],
                                                  [math.sin(params[q]), math.cos(params[q])]]))

        for layer in range(self.n_layers):
            for q in range(self.n_qubits - 1):
                state = self._apply_2q_gate(state, self.n_qubits, q, q + 1, np.array([
                    [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]))

            offset = self.n_qubits + layer * self.n_qubits
            for q in range(self.n_qubits):
                theta = params[offset + q] if offset + q < len(params) else 0.01
                state = self._apply_1q_gate(state, self.n_qubits, q,
                                            np.array([[math.cos(theta), -math.sin(theta)],
                                                      [math.sin(theta), math.cos(theta)]]))

        return state

    def solve(self, hamiltonian: np.ndarray,
              initial_params: Optional[np.ndarray] = None,
              max_iterations: int = 500) -> VQEResult:
        n_params = self.n_qubits + self.n_layers * self.n_qubits
        if initial_params is None:
            params = np.random.uniform(-0.1, 0.1, n_params)
        else:
            params = np.array(initial_params[:n_params])

        convergence = []
        best_energy = float('inf')
        best_params = params.copy()

        for iteration in range(max_iterations):
            state = self._hardware_efficient_ansatz(params)
            energy = np.real(np.dot(state.conj(), hamiltonian @ state))
            convergence.append(float(energy))

            if energy < best_energy:
                best_energy = float(energy)
                best_params = params.copy()

            epsilon = 0.001
            for i in range(len(params)):
                params_plus = params.copy()
                params_plus[i] += epsilon
                state_plus = self._hardware_efficient_ansatz(params_plus)
                energy_plus = np.real(np.dot(state_plus.conj(), hamiltonian @ state_plus))

                params_minus = params.copy()
                params_minus[i] -= epsilon
                state_minus = self._hardware_efficient_ansatz(params_minus)
                energy_minus = np.real(np.dot(state_minus.conj(), hamiltonian @ state_minus))

                grad = (energy_plus - energy_minus) / (2.0 * epsilon)
                params[i] -= 0.01 * grad

            if len(convergence) > 20:
                if abs(convergence[-1] - convergence[-20]) < 1e-8:
                    break

        return VQEResult(
            optimal_parameters=list(best_params),
            optimal_energy=best_energy,
            n_iterations=iteration + 1,
            convergence=convergence,
            ansatz_depth=self.n_layers,
            n_qubits=self.n_qubits,
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

    @staticmethod
    def _apply_2q_gate(state: np.ndarray, n_qubits: int, q1: int, q2: int,
                        gate: np.ndarray) -> np.ndarray:
        dim = len(state)
        new_state = np.zeros(dim, dtype=complex)
        for k in range(dim):
            b1 = (k >> q1) & 1
            b2 = (k >> q2) & 1
            row = (b1 << 1) | b2
            for col in range(4):
                t1 = (col >> 1) & 1
                t2 = col & 1
                if t1 != b1:
                    src = k ^ (1 << q1)
                else:
                    src = k ^ (1 << q2)
                j = src
                new_state[k] += gate[row, col] * state[j]
        return new_state
