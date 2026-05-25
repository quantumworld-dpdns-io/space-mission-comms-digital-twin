from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np


@dataclass
class AnnealingResult:
    final_state: list[int] = field(default_factory=list)
    final_energy: float = 0.0
    energy_history: list[float] = field(default_factory=list)
    n_steps: int = 0
    schedule: str = "linear"


class QuantumAnnealing:
    def __init__(self, n_qubits: int = 4):
        self.n_qubits = n_qubits

    def build_ising(self, J: np.ndarray, h: np.ndarray) -> np.ndarray:
        return J, h

    def simulate(self, J: np.ndarray, h: np.ndarray,
                 n_steps: int = 1000, temperature: float = 1.0,
                 schedule: str = "linear") -> AnnealingResult:
        spins = np.random.choice([-1, 1], self.n_qubits)
        energy_history = []

        for step in range(n_steps):
            s = step / n_steps
            if schedule == "linear":
                A, B = 1.0 - s, s
            elif schedule == "exponential":
                A = math.exp(-5 * s)
                B = 1.0 - A
            else:
                A, B = 1.0 - s, s

            current_energy = self._ising_energy(spins, J, h)

            i = np.random.randint(0, self.n_qubits)
            spins[i] *= -1
            new_energy = self._ising_energy(spins, J, h)
            delta = new_energy - current_energy

            if delta > 0 and np.random.random() > math.exp(-delta / (B * temperature)):
                spins[i] *= -1
            else:
                current_energy = new_energy

            total_energy = current_energy
            energy_history.append(float(total_energy))

        return AnnealingResult(
            final_state=list(spins),
            final_energy=energy_history[-1] if energy_history else 0.0,
            energy_history=energy_history,
            n_steps=n_steps,
            schedule=schedule,
        )

    def _ising_energy(self, spins: np.ndarray, J: np.ndarray, h: np.ndarray) -> float:
        energy = -np.dot(h, spins)
        for i in range(self.n_qubits):
            for j in range(i + 1, self.n_qubits):
                energy -= J[i, j] * spins[i] * spins[j]
        return energy

    def build_qubo(self, Q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        n = Q.shape[0]
        h = np.zeros(n)
        J = np.zeros((n, n))
        for i in range(n):
            h[i] = -0.5 * Q[i, i] - 0.25 * sum(Q[i, j] + Q[j, i] for j in range(n) if j != i)
            for j in range(i + 1, n):
                J[i, j] = 0.25 * (Q[i, j] + Q[j, i])
        return J, h
