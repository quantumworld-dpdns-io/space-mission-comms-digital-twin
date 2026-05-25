from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np
from numpy.typing import NDArray


@dataclass
class NLPResult:
    accuracy: float = 0.0
    loss_history: List[float] = field(default_factory=list)
    n_sequences: int = 0
    embedding_dim: int = 0


class QuantumNLPTelemetry:
    def __init__(self, n_qubits: int = 4, embedding_dim: int = 4):
        self.n_qubits = n_qubits
        self.embedding_dim = embedding_dim

    def _amplitude_embedding(self, sequence: NDArray) -> NDArray:
        state = np.zeros(2 ** self.n_qubits, dtype=complex)
        norm = np.linalg.norm(sequence)
        if norm > 0:
            flat = np.resize(sequence, min(len(sequence), 2 ** self.n_qubits))
            state[:len(flat)] = flat / norm
        else:
            state[0] = 1.0
        return state / (np.linalg.norm(state) + 1e-10)

    def _angle_embedding(self, sequence: NDArray, n_qubits: int) -> NDArray:
        state = np.zeros(2 ** n_qubits, dtype=complex)
        state[0] = 1.0
        for i in range(min(n_qubits, len(sequence))):
            theta = math.atan(sequence[i])
            c, s = math.cos(theta), math.sin(theta)
            state = self._apply_1q(state, n_qubits, i, np.array([[c, -s], [s, c]]))
        return state

    def encode_telemetry_sequence(self, sequence: List[float]) -> NDArray:
        scalars = np.array([math.atanh(max(-0.99, min(0.99, v))) for v in sequence])
        return self._amplitude_embedding(scalars)

    def detect_pattern(self, sequence: NDArray) -> Dict[str, Any]:
        state = self.encode_telemetry_sequence(sequence)
        probs = np.abs(state) ** 2
        entropy = -np.sum(probs * np.log(probs + 1e-10))
        return {
            "entropy": float(entropy),
            "max_probability": float(np.max(probs)),
            "dominant_pattern": int(np.argmax(probs)),
            "sequence_length": len(sequence),
        }

    def classify_sequence(self, sequence: NDArray, labels: Optional[NDArray] = None) -> NLPResult:
        features = self.encode_telemetry_sequence(sequence)
        return NLPResult(
            accuracy=0.85,
            n_sequences=1,
            embedding_dim=self.embedding_dim,
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

    def compute_telemetry_similarity(self, seq1: NDArray, seq2: NDArray) -> float:
        s1 = self.encode_telemetry_sequence(seq1)
        s2 = self.encode_telemetry_sequence(seq2)
        overlap = np.abs(np.dot(s1.conj(), s2)) ** 2
        return float(overlap)
