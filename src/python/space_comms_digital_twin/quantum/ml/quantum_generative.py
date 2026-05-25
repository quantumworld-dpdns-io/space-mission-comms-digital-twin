from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass
class GenerativeResult:
    samples: list[list[int]] = field(default_factory=list)
    fidelity: float = 0.0
    n_parameters: int = 0
    training_loss: list[float] = field(default_factory=list)


class QuantumGenerativeModel:
    def __init__(self, n_qubits: int = 4, n_layers: int = 2):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.n_params = n_qubits * (n_layers + 1)
        self.params = np.random.uniform(-0.1, 0.1, self.n_params)

    def _born_machine(self, params: NDArray) -> NDArray:
        state = np.zeros(2 ** self.n_qubits, dtype=complex)
        state[0] = 1.0

        for q in range(self.n_qubits):
            theta = params[q]
            c, s = math.cos(theta), math.sin(theta)
            state = self._apply_1q(state, self.n_qubits, q, np.array([[c, -s], [s, c]]))

        for layer in range(self.n_layers):
            for q in range(self.n_qubits - 1):
                state = self._apply_cnot(state, self.n_qubits, q, q + 1)
            offset = self.n_qubits + layer * self.n_qubits
            for q in range(self.n_qubits):
                if offset + q < len(params):
                    theta = params[offset + q]
                    c, s = math.cos(theta), math.sin(theta)
                    state = self._apply_1q(state, self.n_qubits, q, np.array([[c, -s], [s, c]]))

        return state

    def sample(self, n_samples: int = 100) -> GenerativeResult:
        state = self._born_machine(self.params)
        probs = np.abs(state) ** 2
        samples = np.random.choice(2 ** self.n_qubits, size=n_samples, p=probs / probs.sum())

        bit_samples = []
        for s in samples:
            bits = [(s >> q) & 1 for q in range(self.n_qubits)]
            bit_samples.append(bits)

        return GenerativeResult(
            samples=bit_samples,
            fidelity=float(np.max(probs)),
            n_parameters=self.n_params,
        )

    def train(self, target_distribution: NDArray, epochs: int = 100) -> GenerativeResult:
        losses = []
        for _epoch in range(epochs):
            state = self._born_machine(self.params)
            current_probs = np.abs(state) ** 2
            current_probs = current_probs / (current_probs.sum() + 1e-10)

            eps = 1e-10
            loss = -np.sum(target_distribution * np.log(current_probs + eps))
            losses.append(float(loss))

            epsilon = 0.01
            for i in range(len(self.params)):
                params_p = self.params.copy()
                params_p[i] += epsilon
                state_p = self._born_machine(params_p)
                probs_p = np.abs(state_p) ** 2
                probs_p = probs_p / (probs_p.sum() + 1e-10)
                loss_p = -np.sum(target_distribution * np.log(probs_p + eps))

                params_m = self.params.copy()
                params_m[i] -= epsilon
                state_m = self._born_machine(params_m)
                probs_m = np.abs(state_m) ** 2
                probs_m = probs_m / (probs_m.sum() + 1e-10)
                loss_m = -np.sum(target_distribution * np.log(probs_m + eps))

                grad = (loss_p - loss_m) / (2 * epsilon)
                self.params[i] -= 0.01 * grad

            if len(losses) > 10 and abs(losses[-1] - losses[-10]) < 1e-6:
                break

        return GenerativeResult(
            samples=[],
            fidelity=1.0 / (len(np.unique(target_distribution)) + 1),
            n_parameters=self.n_params,
            training_loss=losses,
        )

    @staticmethod
    def _apply_1q(state: NDArray, n_qubits: int, qubit: int, gate: NDArray) -> NDArray:
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
    def _apply_cnot(state: NDArray, n_qubits: int, control: int, target: int) -> NDArray:
        dim = len(state)
        new_state = np.zeros(dim, dtype=complex)
        for k in range(dim):
            if (k >> control) & 1:
                new_state[k] = state[k ^ (1 << target)]
            else:
                new_state[k] = state[k]
        return new_state
