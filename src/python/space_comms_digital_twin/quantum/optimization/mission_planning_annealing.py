from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from space_comms_digital_twin.quantum.optimization.quantum_annealing import (
    AnnealingResult,
    QuantumAnnealing,
)


@dataclass
class MissionPlanningProblem:
    n_tasks: int = 0
    priorities: list[float] = field(default_factory=list)
    durations: list[float] = field(default_factory=list)
    conflicts: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))
    weather_dependency: list[float] = field(default_factory=list)
    deadline: float = 0.0


class MissionPlanningAnnealing:
    def __init__(self, n_qubits: int = 6):
        self.n_qubits = n_qubits
        self.annealer = QuantumAnnealing(n_qubits=n_qubits)

    def build_problem(self, tasks: list[dict[str, Any]],
                      deadline: float) -> MissionPlanningProblem:
        n = len(tasks)
        priorities = [t.get("priority", 1) for t in tasks]
        durations = [t.get("duration", 1) for t in tasks]
        weather = [t.get("weather_dependency", 0.0) for t in tasks]

        conflicts = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                if (tasks[i]["start"] < tasks[j]["end"] and
                        tasks[j]["start"] < tasks[i]["end"]):
                    conflicts[i, j] = 1.0
                    conflicts[j, i] = 1.0

        return MissionPlanningProblem(
            n_tasks=n,
            priorities=priorities,
            durations=durations,
            conflicts=conflicts,
            weather_dependency=weather,
            deadline=deadline,
        )

    def solve(self, problem: MissionPlanningProblem,
              n_steps: int = 1000) -> AnnealingResult:
        n = min(problem.n_tasks, self.n_qubits)
        if n == 0:
            return AnnealingResult()

        J = np.zeros((n, n))
        h = np.zeros(n)

        for i in range(n):
            h[i] = problem.priorities[i] / (max(problem.priorities) + 1e-6)
            if problem.weather_dependency[i] > 0.5:
                h[i] *= 0.5
            for j in range(i + 1, n):
                if problem.conflicts[i, j] > 0:
                    J[i, j] = -2.0 * h[i] * h[j]

        result = self.annealer.simulate(J, h, n_steps=n_steps)

        return result
