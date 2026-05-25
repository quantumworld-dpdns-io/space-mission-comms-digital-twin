from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from space_comms_digital_twin.quantum.optimization.qaoa import QAOA, QAOResult


@dataclass
class AntennaScheduleProblem:
    n_antennas: int = 0
    n_time_slots: int = 0
    n_tasks: int = 0
    task_weights: list[float] = field(default_factory=list)
    overlap_matrix: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))
    time_windows: list[tuple[int, int]] = field(default_factory=list)
    antenna_task_map: dict[int, list[int]] = field(default_factory=dict)


class AntennaSchedulingQAOA:
    def __init__(self, n_layers: int = 1):
        self.n_layers = n_layers
        self.qaoa = QAOA(n_layers=n_layers)

    def build_problem(self, n_antennas: int, n_time_slots: int,
                      tasks: list[dict[str, Any]]) -> AntennaScheduleProblem:
        n_tasks = len(tasks)
        task_weights = [t.get("priority", 1) for t in tasks]
        overlap = np.zeros((n_tasks, n_tasks))
        for i in range(n_tasks):
            for j in range(i + 1, n_tasks):
                tw_i = (tasks[i]["start"], tasks[i]["end"])
                tw_j = (tasks[j]["start"], tasks[j]["end"])
                if max(tw_i[0], tw_j[0]) < min(tw_i[1], tw_j[1]):
                    overlap[i, j] = 1.0
                    overlap[j, i] = 1.0

        return AntennaScheduleProblem(
            n_antennas=n_antennas,
            n_time_slots=n_time_slots,
            n_tasks=n_tasks,
            task_weights=task_weights,
            overlap_matrix=overlap,
            time_windows=[(t.get("start", 0), t.get("end", n_time_slots)) for t in tasks],
        )

    def solve(self, problem: AntennaScheduleProblem) -> QAOResult:
        n_qubits = problem.n_tasks * problem.n_antennas
        if n_qubits == 0:
            return QAOResult()

        edges = []
        for i in range(problem.n_tasks):
            for a in range(problem.n_antennas):
                v = i * problem.n_antennas + a
                for j in range(i + 1, problem.n_tasks):
                    if problem.overlap_matrix[i, j] > 0:
                        for b in range(problem.n_antennas):
                            w = j * problem.n_antennas + b
                            if a == b:
                                edges.append((v, w))

        if not edges:
            n_qubits_small = max(1, min(10, n_qubits))
            edges = [(0, 1)]

        H = self.qaoa.build_maxcut_hamiltonian(edges, n_qubits_small if n_qubits > 10 else n_qubits)
        result = self.qaoa.solve(H)

        return result
