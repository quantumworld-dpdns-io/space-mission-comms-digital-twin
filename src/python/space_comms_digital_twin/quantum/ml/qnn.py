from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass
class QNNResult:
    accuracy: float = 0.0
    loss_history: list[float] = field(default_factory=list)
    n_epochs: int = 0
    n_parameters: int = 0
    final_loss: float = 0.0


class QNN:
    def __init__(self, n_qubits: int = 4, n_layers: int = 2,
                 learning_rate: float = 0.01):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.lr = learning_rate
        self.n_params = n_qubits * (n_layers + 1)
        self.params = np.random.uniform(-0.1, 0.1, self.n_params)

    def _encode_input(self, x: NDArray) -> NDArray:
        state = np.zeros(2 ** self.n_qubits, dtype=complex)
        state[0] = 1.0
        for i in range(min(self.n_qubits, len(x))):
            theta = math.atan(x[i])
            c, s = math.cos(theta / 2), math.sin(theta / 2)
            state = self._apply_1q_gate(state, self.n_qubits, i,
                                        np.array([[c, -s], [s, c]]))
        return state

    def _variational_circuit(self, state: NDArray, params: NDArray) -> NDArray:
        for q in range(self.n_qubits):
            theta = params[q]
            c, s = math.cos(theta), math.sin(theta)
            state = self._apply_1q_gate(state, self.n_qubits, q,
                                        np.array([[c, -s], [s, c]]))

        for layer in range(self.n_layers):
            for q in range(self.n_qubits - 1):
                state = self._apply_2q_gate(state, self.n_qubits, q, q + 1)

            offset = self.n_qubits + layer * self.n_qubits
            for q in range(self.n_qubits):
                if offset + q < len(params):
                    theta = params[offset + q]
                    c, s = math.cos(theta), math.sin(theta)
                    state = self._apply_1q_gate(state, self.n_qubits, q,
                                                np.array([[c, -s], [s, c]]))
        return state

    def fit(self, X: NDArray, y: NDArray, epochs: int = 50,
            batch_size: int = 32) -> QNNResult:
        n = len(X)
        loss_history = []

        for _epoch in range(epochs):
            idx = np.random.permutation(n)
            epoch_loss = 0.0
            n_batches = max(1, n // batch_size)

            for batch in range(n_batches):
                batch_idx = idx[batch * batch_size: (batch + 1) * batch_size]
                batch_X = X[batch_idx]
                batch_y = y[batch_idx]

                grads = np.zeros_like(self.params)
                loss = 0.0
                epsilon = 0.001

                for i, x in enumerate(batch_X):
                    state = self._encode_input(x)
                    output = self._variational_circuit(state, self.params)
                    pred = np.real(np.dot(output.conj(), output))
                    expected = float(batch_y[i])
                    loss += (pred - expected) ** 2

                    for j in range(len(self.params)):
                        params_p = self.params.copy()
                        params_p[j] += epsilon
                        output_p = self._variational_circuit(state, params_p)
                        pred_p = np.real(np.dot(output_p.conj(), output_p))

                        params_m = self.params.copy()
                        params_m[j] -= epsilon
                        output_m = self._variational_circuit(state, params_m)
                        pred_m = np.real(np.dot(output_m.conj(), output_m))

                        grads[j] += 2 * (pred - expected) * (pred_p - pred_m) / (2 * epsilon)

                self.params -= self.lr * grads / len(batch_idx)
                epoch_loss += loss / len(batch_idx)

            avg_loss = epoch_loss / n_batches
            loss_history.append(float(avg_loss))

        predictions = self.predict(X)
        accuracy = float(np.mean(predictions == y))

        return QNNResult(
            accuracy=accuracy,
            loss_history=loss_history,
            n_epochs=epochs,
            n_parameters=self.n_params,
            final_loss=loss_history[-1] if loss_history else 0.0,
        )

    def predict(self, X: NDArray) -> NDArray:
        predictions = []
        for x in X:
            state = self._encode_input(x)
            output = self._variational_circuit(state, self.params)
            prob = float(np.real(np.dot(output.conj(), output)))
            predictions.append(1 if prob > 0.5 else 0)
        return np.array(predictions)

    @staticmethod
    def _apply_1q_gate(state: NDArray, n_qubits: int, qubit: int,
                        gate: NDArray) -> NDArray:
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
    def _apply_2q_gate(state: NDArray, n_qubits: int, q1: int, q2: int) -> NDArray:
        dim = len(state)
        new_state = np.zeros(dim, dtype=complex)
        for k in range(dim):
            b1 = (k >> q1) & 1
            (k >> q2) & 1
            if b1 == 1:
                target = k ^ (1 << q2)
                new_state[k] = state[target]
            else:
                new_state[k] = state[k]
        return new_state
